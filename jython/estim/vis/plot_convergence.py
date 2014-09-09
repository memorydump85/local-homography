import sys
import util.jsonx as jsonx
import numpy as np
from matplotlib import pyplot, cm
import matplotlib


if __name__ == '__main__':
#--------------------------------------
    font = {'size': 10}
    matplotlib.rc('font', **font)
    
    convergence_data = jsonx.load_file(sys.argv[1])
    classic = np.zeros((10,10))
    augmented = np.zeros((10,10))
    
    cmap = cm.get_cmap('PiYG')
    
    for xy, info in convergence_data.iteritems():
        coord = xy.split(',')
        x, y = int(coord[0]), int(coord[1])
        x, y = (x-200)/40, (y-200)/40
        
        if len(info.classic)==0: info.classic = [0, 0, 0, 0]

        k = np.array([373.0, 373.0, 404.0, 250.0])
        classic[x,y] = np.linalg.norm(k-info.classic)
        augmented[x,y] = np.linalg.norm(k-info.augmented)

    print min(augmented.flatten())
    print max(augmented.flatten())

    clim = (0, 6000)
    pyplot.subplot(3,2,1)
    pyplot.title("Tamron 2.2 - Classic")
    pyplot.imshow(classic, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
    
    pyplot.subplot(3,2,2)
    pyplot.title("Tamron 2.2 - Augmented")
    pyplot.imshow(augmented, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
    

    convergence_data = jsonx.load_file(sys.argv[2])
    classic = np.zeros((10,10))
    augmented = np.zeros((10,10))
    
    cmap = cm.get_cmap('PiYG')
    
    for xy, info in convergence_data.iteritems():
        coord = xy.split(',')
        x, y = int(coord[0]), int(coord[1])
        x, y = (x-200)/40, (y-200)/40
        
        if len(info.classic)==0: info.classic = [0, 0, 0, 0]

        k = np.array([373.0, 373.0, 404.0, 250.0])
        classic[x,y] = np.linalg.norm(k-info.classic)
        augmented[x,y] = np.linalg.norm(k-info.augmented)

    print min(augmented.flatten())
    print max(augmented.flatten())

    clim = (0, 3000)
    pyplot.subplot(3,2,3)
    pyplot.title("Tamron 2.8 - Classic")
    pyplot.imshow(classic, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
    
    pyplot.subplot(3,2,4)
    pyplot.title("Tamron 2.8 - Augmented")
    pyplot.imshow(augmented, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
    

    convergence_data = jsonx.load_file(sys.argv[3])
    classic = np.zeros((10,10))
    augmented = np.zeros((10,10))
    
    cmap = cm.get_cmap('PiYG')
    
    for xy, info in convergence_data.iteritems():
        coord = xy.split(',')
        x, y = int(coord[0]), int(coord[1])
        x, y = (x-200)/40, (y-200)/40
        
        if len(info.classic)==0: info.classic = [0, 0, 0, 0]

        k = np.array([373.0, 373.0, 404.0, 250.0])
        classic[x,y] = np.linalg.norm(k-info.classic)
        augmented[x,y] = np.linalg.norm(k-info.augmented)

    print min(augmented.flatten())
    print max(augmented.flatten())

    clim = (0, 5000)
    pyplot.subplot(3,2,5)
    pyplot.title("Tokina 3.3 - Classic")
    pyplot.imshow(classic, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
    
    pyplot.subplot(3,2,6)
    pyplot.title("Tokina 3.3 - Augmented")    
    pyplot.imshow(augmented, cmap=cmap, interpolation=None, extent=(200,560,200,560))
    pyplot.locator_params(nbins=4)
    pyplot.grid()
    pyplot.clim(clim)
    pyplot.colorbar(ticks=(clim[0], clim[1]/2, clim[1]))
        
    pyplot.show()