import numpy as np
import util.jsonx as jsonx
from mathx.gp import GaussianProcess, sqexp2D_covariancef


#--------------------------------------
class PolyUndistortionModel(object):
#--------------------------------------
    def __init__(self, jsonfile):
        with open(jsonfile) as f:
            distortion_info = jsonx.load(f)
            self.poly_terms = compile(distortion_info.poly_terms, '', 'eval')
            self.poly_x = distortion_info.poly_x
            self.poly_y = distortion_info.poly_y

            
    def undistort(self, i, j):
        phi = np.array(eval(self.poly_terms))
        return (i + phi.dot(self.poly_x), j + phi.dot(self.poly_y))


#--------------------------------------
class GPUndistortionModel(object):
#--------------------------------------
    def __init__(self, jsonfile):
        with open(jsonfile) as f:
            dinf = jsonx.load(f)
            xinf = dinf.gp_x
            yinf = dinf.gp_y
            
            self.gp_x = GaussianProcess(np.array(xinf.x),
                                        np.array(xinf.t),
                                        sqexp2D_covariancef(np.array(xinf.hypparams)))
            self.gp_y = GaussianProcess(np.array(yinf.x),
                                        np.array(yinf.t),
                                        sqexp2D_covariancef(np.array(yinf.hypparams)))
            self.mean_x = xinf.mean
            self.mean_y = yinf.mean

            
    def undistort(self, i, j):
        di = i + self.mean_x + self.gp_x.predict([(i, j)])[0]
        dj = j + self.mean_y + self.gp_y.predict([(i, j)])[0]
        return (di, dj)