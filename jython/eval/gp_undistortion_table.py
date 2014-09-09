import sys
import numpy as np
from multiprocessing import Pool
from estim.undistortion_model import GPUndistortionModel
import util.jsonx as jsonx


if __name__ == '__main__':
#--------------------------------------
    model = GPUndistortionModel(sys.argv[1])
    W, H = jsonx.load_file(sys.argv[2]).iteritems().next()[1].size
    
    def undistort_column(x):
        sys.stderr.write('    Undistorting col %d\r' % x)
        points = [(x,j) for j in range(H)]

        ux = model.gp_x.predict(points)
        uy = model.gp_y.predict(points)
        displaced = points + np.vstack((ux, uy)).T

        ret = {}
        for p, d in zip(points, displaced):
            ret[repr(p)] = d.tolist()

        return ret
    
    
    pool = Pool()
    results = pool.map(undistort_column, range(W))
    
    pool.close()
    pool.join()
    
    sys.stderr.write('\n')
    undistorted = {}
    for d in results: undistorted.update(d)
    jsonx.dump(undistorted, sys.stdout)