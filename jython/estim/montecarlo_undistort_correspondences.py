import sys
from copy import deepcopy
import numpy as np
import simplejson
from undistortion_model import GPUndistortionModel


if __name__ == '__main__':
#--------------------------------------
    correspondences = simplejson.load(open(sys.argv[1]))
    model = GPUndistortionModel(sys.argv[2])
    
    samples = {}
    for name, info in correspondences.iteritems():
        data = np.array([(int(i), d[u'tgt'][0], d[u'tgt'][1]) for i, d in info[u'detections'].iteritems()])
        query = data[:,1:]
        predict_x = model.gp_x.predict(query, cov=True)
        predict_y = model.gp_y.predict(query, cov=True)
        
        # distort the query points using mutiple samples from the GP
        NSAMPLES=10
        query = query + [model.mean_x, model.mean_y]
        gx = np.random.multivariate_normal(predict_x[0], predict_x[1], NSAMPLES)
        gy = np.random.multivariate_normal(predict_y[0], predict_y[1], NSAMPLES)
        
        for i, sx, sy in zip(range(NSAMPLES), gx, gy):
            tgt = query + np.vstack((sx, sy)).T
            sample_info = deepcopy(info)
            for j in range(len(data)):
                tagid = str(int(data[j,0]))
                sample_info[u'detections'][tagid][u'tgt'] = list(tgt[j]) 
            samples[name + '_' + str(i)] = sample_info 
                
    simplejson.dump(samples, sys.stdout, indent=2)