import sys
from math import sqrt
import fileinput
import util.jsonx as jsonx
from raymap.math import WeightedLocalHomography, SqExpWeightingFunction
from april.jmat import LinAlg


phi = (1 + sqrt(5))/2
resphi = 2 - phi

sqdist = lambda p, q: (p[0]-q[0])**2 + (p[1]-q[1])**2
homogenize = lambda a: list(a) + [1.]
normalize = lambda a: [a[0]/a[2], a[1]/a[2], 1] 


def goldenSectionSearch(f, a, c, b, absolutePrecision):
#--------------------------------------    
#    Any reasonable person will use Brent's method instead of
#    the goldenSectionSearch. But then scipy.optimize is not
#    accessible in Jython and hence ...
#    
#    `a` and `b` are the current bounds; the minimum is between them.
#    `c` is the center pointer pushed slightly left towards `a`
#    from: https://gist.github.com/crankycoder/649552
#    
    if abs(a - b) < absolutePrecision:
        return a if f(a) < f(b) else b 
    # Create a new possible center, in the area between c and b, pushed against c
    d = c + resphi*(b - c)
    if f(d) < f(c):
        return goldenSectionSearch(f, c, d, b, absolutePrecision)
    else:
        return goldenSectionSearch(f, d, c, a, absolutePrecision)


def build_weighted_homography(corrs, tau):
#--------------------------------------
    wh = WeightedLocalHomography()
    for c in corrs: wh.addCorrespondence(c[0:2], c[2:4])
    wh.setWeightingFunction(SqExpWeightingFunction(tau))
    
    return wh


def test_error(train, testPt, tau, details=False):
#--------------------------------------
#    Compute test error of WeightedLocalHomography with bandwidth `tau`
#    The weighted homography is fit using `train` correspondences. The
#    resulting homography is used to test the error at testPt
#
    wh = build_weighted_homography(train, tau)
        
    p = homogenize(testPt[0:2])
    q = normalize(wh.map(p))
    
    err = sqrt(sqdist(q, testPt[2:4]))
    if details:
        return (err, wh.getHomographyAt(p))
    else:
        return err


def optimal_homography_at(pt, correspondences, a, c, b, absolutePrecision):
#--------------------------------------
    objf = lambda t: test_error(correspondences, pt, t)
    optimum = goldenSectionSearch(objf, a=a, c=c, b=b, absolutePrecision=absolutePrecision)
    
    err, h_array = test_error(correspondences, pt, optimum, details=True)
    return dict(weighting_sigma=optimum,
                homography_err=round(err, 4),
                homography=h_array,
                correspondence=pt)


def process_image(iminfo):
#--------------------------------------
    width, height = iminfo.size
    cxy = [width/2., height/2.]
    
    # Correspondences Sort by distance to image center
    wi = [(d.src[0], d.src[1], d.tgt[0], d.tgt[1])
                  for tagid, d in iminfo.detections.iteritems()]
    wi.sort(lambda a, b: sqdist(a[2:4], cxy) - sqdist(b[2:4], cxy))
    iw = [(ix, iy, wx, wy) for wx, wy, ix, iy in wi]
    
    # Find optimal weighting bandwidth
    r1 = optimal_homography_at(iw[0], iw[1:], a=1000, c=5000, b=10000, absolutePrecision=0.01)
    
    # Find homography at center
    wh = build_weighted_homography(iw, r1['weighting_sigma'])
    
    # Where does the center of the image project to?
    wc = normalize(wh.map(homogenize(cxy)))
    corr = (wc[0]/wc[2], wc[1]/wc[2], cxy[0], cxy[1])
    
    # Now, the optimal homography (world to image) at the center of the image
    r2 = optimal_homography_at(corr, wi, a=0.0001, c=0.09, b=0.1, absolutePrecision=0.01)
    
    flatten = lambda A: [e for row in A for e in row]
    r1['homography'] = flatten(r1['homography'])
    r2['homography'] = flatten(r2['homography'])
    
    return dict(image_to_world=r1, world_to_image=r2)


if __name__ == "__main__":
#--------------------------------------    
    estimates = {}
    for name, info in jsonx.load(open(sys.argv[1])).iteritems():
        estimates[name] = process_image(info)
        
    jsonx.dump(estimates, sys.stdout)