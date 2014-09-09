import sys
import util.jsonx as jsonx
from undistortion_model import GPUndistortionModel, PolyUndistortionModel


if __name__ == '__main__':
#--------------------------------------
    correspondences = jsonx.load_file(sys.argv[1])
    model = GPUndistortionModel(sys.argv[2])
    
    for name, info in correspondences.iteritems():
        for tagid, detinfo in info.detections.iteritems():
            detinfo[u'tgt'] = model.undistort(*detinfo.tgt)
            
    jsonx.dump(correspondences, sys.stdout)