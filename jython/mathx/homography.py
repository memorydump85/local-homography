import numpy as np
from numpy.linalg import norm, svd


#--------------------------------------
class WeightedLocalHomography(object):
#--------------------------------------
#
#    BUGGY! Need to verify by comparing with Java version
#
    corrs = None
    
    xformSource = None
    xformTarget = None
    
    
    def __init__(self, weightingFunction=lambda a,b:1, regularizationLambda=0):
        self.wgtFn = weightingFunction
        self.rLambda = regularizationLambda
    
        
    def add_correspondence(self, sourcex, sourcey, targetx, targety):
        c = np.array((sourcex, sourcey, targetx, targety))
        self.corrs = np.array(c) if self.corrs is None \
                                 else np.vstack((self.corrs, c))
        self.xformSource = None
        self.xformTarget = None
    
                                 
    def map(self, srcPt):
        H = self.homography_at(srcPt)
        return np.dot(H, srcPt)
    
    
    def homography_at(self, srcPt):
        if self.xformSource is None or self.xformTarget is None:
            self.xformSource = Transforms2D.meanshift(self.corrs[:,0:2])
            self.xformTarget = Transforms2D.meanshift(self.corrs[:,2:4])

            self.A = []
            for corr in self.corrs:
                src = np.dot(self.xformSource.A, np.array([corr[0], corr[1], 1]).T)
                tgt = np.dot(self.xformTarget.A, np.array([corr[2], corr[3], 1]).T)

                x, y = src[0], src[1]
                i, j = tgt[0], tgt[1]
                
                self.A.append([-x, -y, -1,  0,  0,  0, i*x, i*y, i])
                self.A.append([ 0,  0,  0, -x, -y, -1, j*x, j*y, j])         
            self.A = np.matrix(self.A)
            
        # Compute weights
        w_diag = []
        for corr in self.corrs:
            w = np.sqrt(self.wgtFn(srcPt, corr[0:2]))
            w_diag.extend([w, w])
            
        lambdaI = np.identity((len(self.A))) * self.rLambda
        W = np.diag(w_diag) + lambdaI
        u, s, v = svd(W.dot(self.A))
        H = v[:,-1].reshape((3,3))
        
        return (self.xformTarget.I * H * self.xformSource).A
    
    class sqexp_weighting(object):
        def __init__(self, tau):
            cov = np.diag([tau, tau])
            self.covInv = np.linalg.inv(cov)
            self.Z = 1.0 / np.sqrt((2*np.pi)**2*np.linalg.det(cov))
        def __call__(self, a, b):
            z = np.array(a[0:2] - b[0:2])
            return self.Z*np.exp(-0.5*z.dot(self.covInv.dot(z)))

    
#--------------------------------------    
class Transforms2D:
#--------------------------------------    
    @staticmethod
    def meanshift(data):
        m = np.mean(data, axis=0)
        return np.matrix([1, 0, -m[0], 0, 1, -m[1], 0, 0, 1]).reshape((3,3))
    
    @staticmethod
    def standardize(data):
        m = np.mean(data, axis=0)
        s = 1.0 / np.std(data, axis=0)
        t = -m[0]*s[0], -m[1]*s[1];
        return np.matrix([s[0], 0, t[0], 0, s[1], t[1], 0, 0, 1]).reshape((3,3))


def homography_to_pose(fx, fy, cx, cy, h):
#--------------------------------------
#
#    BUGGY! Need to verify by comparing with Java version
#
    M = np.zeros((4,4))
    M[0,0] =  (h[0,0]-cx*h[2,0]) / fx;
    M[0,1] =  (h[0,1]-cx*h[2,1]) / fx;
    M[0,3] =  (h[0,2]-cx*h[2,2]) / fx;
    M[1,0] =  (h[1,0]-cy*h[2,0]) / fy;
    M[1,1] =  (h[1,1]-cy*h[2,1]) / fy;
    M[1,3] =  (h[1,2]-cy*h[2,2]) / fy;
    M[2,0] =  h[2,0];
    M[2,1] =  h[2,1];
    M[2,3] =  h[2,2];
    M[3,3] =  1; # will get overwritten anyway.
    
    # Compute the scale. The columns of M should be made to be
    # unit vectors. This is over-determined, so we take the
    # geometric average.
    scale = np.sqrt(norm(M[:,0])*norm(M[:,1]));
    M = M / scale;
    
    # recover sign of scale factor by noting that observations
    # must occur in front of the camera. (which is z < 0).
    if (M[2,3] > 0): M *= -1;
    
    # The bottom row should always be [0 0 0 1].  We reset the
    # first three elements, even though they must be zero, in
    # order to make sure that they are +0. (We could have -0 due
    # to the sign flip above. This is theoretically harmless but
    # annoying in practice.)
    M[3,:] = [0, 0, 0, 1]
    
    # recover third rotation vector by crossproduct of the other two rotation vectors.
    M[:,2] = np.cross(M[:,0], M[:,1])
    
    # pull out just the rotation component so we can normalize it.
    R = M[0:3,0:3]
    
    U, _, V = svd(R)
    # polar decomposition, R = (UV')(VSV')
    M[0:3,0:3] = U*V.T
    return M;