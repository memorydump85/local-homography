import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys
import itertools
from mathx.gp import GaussianProcess, sqexp2D_covariancef
from estim.undistortion_model import *


if __name__ == '__main__':
#--------------------------------------
    font = {'size': 11}
    matplotlib.rc('font', **font)

    
    polymodel = PolyUndistortionModel(sys.argv[1])
    gpmodel = GPUndistortionModel(sys.argv[1])
    undistorts = jsonx.load_file(sys.argv[1])
    
    model = gpmodel
    W, H = jsonx.load_file(sys.argv[2]).iteritems().next()[1].size
       
    # load the original training data
    quiver = []
    for name, data in undistorts.iteritems():
        if name.endswith('.png'): quiver.extend(data)

    # Plot observations
    quiver = np.array(quiver)
    plt.subplot(2,1,1)
    plt.quiver(quiver[:,0], quiver[:,1], quiver[:,2], quiver[:,3], width=0.001, color='b')
    plt.title('Observations')
    plt.xlim([-150, 900])
    plt.ylim([-150, 550])
    
    
    # plot model predictions
    test = np.array([np.array([i,j]) for i in np.arange(0, W, 25) for j in np.arange(0, H, 25)])
    #test = np.concatenate([test, quiver[:,0:2]])
    dtest = np.array([model.undistort(i, j) for (i, j) in test]) - test
    
    plt.subplot(2,1,2)
    plt.quiver(test[:,0], test[:,1], dtest[:,0], dtest[:,1], width=0.001, color='r')
    plt.title('Model')
    #plt.show(block=False)
    plt.xlim([-150, 900])
    plt.ylim([-150, 550])
    plt.show()
     
     
#     # show undistorted points
#     colors = itertools.cycle(['#ff0000', '#00ff00', '#0000ff', '#ff00ff', '#00ffff', '#ffff00'])
#   
#     for imname, info in jsonx.load_file(sys.argv[2]).iteritems():
#         x_vals = []
#         y_vals = []
#         ux_vals = []
#         uy_vals = []
#         for tags, corr in info.detections.iteritems():
#             p = corr.tgt
#             q = model.undistort(p[0], p[1])
#             x_vals.append(p[0]); y_vals.append(p[1])
#             ux_vals.append(q[0]); uy_vals.append(q[1])
#         color = colors.next()
#         plt.subplot(2,2,3)
#         plt.scatter(x_vals, y_vals, c=color, s=15)
#         plt.subplot(2,2,4)
#         plt.scatter(ux_vals, uy_vals, c=color, s=15)
#  
#     plt.show()