import optparse, sys
import util.jsonx as jsonx
import numpy as np
from mathx.gp import GaussianProcess, sqexp2D_covariancef


# 6th order polynomial in i,j
poly_terms = \
'''[ i**5, i**4*j, i**3*j**2, i**2*j**3, i*j**4, j**5,
     i**4, i**3*j, i**2*j**2, i*j**3, j**4,
     i**3, i*i*j, i*j*j, j**3,
     i*i, i*j, j*j,
     i, j,
     1 ] '''

# polynomial feature vector for (i,j)
poly_terms_c = compile(poly_terms, '', 'eval')
phi = lambda i, j: eval(poly_terms_c) 


def poly_regress2D(data, obs):
#--------------------------------------
    Phi = np.array([phi(i, j)  for (i, j) in data])
    return np.linalg.lstsq(Phi, obs)[0]


if __name__ == "__main__":
#--------------------------------------
    # parse options
    optparser = optparse.OptionParser()
    optparser.add_option('--correspondences',
                         action='store', type='string', dest='tagfile',
                         help='JSON data-file containing tag correspondences for an image set')
    optparser.add_option('--homographies',
                         action='store', type='string', dest='hfile',
                         help='JSON data-file containing initial homography estimates for an image set')
    optparser.add_option('--init',
                         action='store', type='string', dest='initfile',
                         help='JSON data-file containing initial homography estimates for an image set')
    opts, _ = optparser.parse_args()
    
    # load files
    tag_correspondences = jsonx.load_file(opts.tagfile)
    homography_inits = jsonx.load_file(opts.hfile)
    gp_init = jsonx.load_file(opts.initfile)

    imsize = None
    undistortion_model = {}
    
    # For each image compute distortion prior by projecting through Homography
    for name, init in homography_inits.iteritems():
        imsize = tag_correspondences[name].size
        undists = []
             
        # Project tags in image through Homography to obtain distortion
        H = np.array(init.world_to_image.homography).reshape(3,3)
        
        for tagid, info in tag_correspondences[name].detections.iteritems():
            w = info.src; w.extend([1])
            w = np.array(w)
            
            v = H.dot(w)
            u = np.array([v[0], v[1]]) / v[2]
            d = np.array(info.tgt)
            
            # d: distorted, u: undistorted
            undists.append([d[0], d[1], u[0]-d[0], u[1]-d[1]])
            
        undistortion_model[name] = undists
    

    # estimate a GP model for the x and y distortions
    data = np.concatenate([d for d in undistortion_model.itervalues()])
    
    undistortion_model['poly_terms'] = poly_terms
    
    x, t = np.array(data[:,0:2]), np.array(data[:,2])
    polymodel_x = poly_regress2D(x, t).tolist()
    undistortion_model['poly_x'] = polymodel_x
        
    x, t = np.array(data[:,0:2]), np.array(data[:,3])
    polymodel_y = poly_regress2D(x, t).tolist()
    undistortion_model['poly_y'] = polymodel_y   
    
    # GP models
    if True:
        W, H = imsize
        tau = gp_init.length_scale
        
        x, t = np.array(data[:,0:2]), np.array(data[:,2])
        mean_t = np.mean(t)
        t = t - mean_t
        theta0 = [np.std(t), tau, tau, 0.0, 100.0]
        gp_dx = GaussianProcess.fit(x, t, sqexp2D_covariancef, theta0)
        undistortion_model['gp_x'] = dict(hypparams=gp_dx.covf.theta.tolist(),
                                         mean=mean_t, x=x.tolist(), t=t.tolist())
        
        x, t = np.array(data[:,0:2]), np.array(data[:,3])        
        mean_t = np.mean(t)
        t = t - mean_t
        theta0 = [np.std(t), tau, tau, 0.0, 100.0]
        gp_dy = GaussianProcess.fit(x, t, sqexp2D_covariancef, theta0)
        undistortion_model['gp_y'] = dict(hypparams=gp_dy.covf.theta.tolist(),
                                         mean=mean_t, x=x.tolist(), t=t.tolist())
        
    
    jsonx.dump(undistortion_model, sys.stdout)