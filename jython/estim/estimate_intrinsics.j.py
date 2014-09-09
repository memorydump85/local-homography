import sys
import util.jsonx as jsonx
from java.util import ArrayList
from april.camera import *
from april.tag import *


if __name__ == '__main__':
#--------------------------------------
    correspondences = jsonx.load_file(sys.argv[1])
    W, H = correspondences.iteritems().next()[1].size
    
    all_detections = ArrayList()
    for _, info in correspondences.iteritems():
        detections = ArrayList()
        for tagid, detinfo in info.detections.iteritems():
            td = TagDetection()
            td.cxy = detinfo.tgt
            td.id = int(tagid)
            detections.add(td)
        
        all_detections.add(detections)
        
    mosaic = TagMosaic(Tag36h11(), 0.0254)
    ie = IntrinsicsEstimator(all_detections, mosaic, W/2., H/2.)
    
    K = ie.getIntrinsics()
    flat = [e for row in K for e in row]
    jsonx.dump(dict(
                    fx=K[0][0], fy=K[1][1],
                    cx=K[0][2], cy=K[1][2],
                    K=flat, bandwidth=0.0001), sys.stdout)