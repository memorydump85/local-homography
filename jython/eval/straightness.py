from __future__ import with_statement
import sys
import util.jsonx as jsonx
import numpy as np
from estim.undistortion_model import PolyUndistortionModel, GPUndistortionModel


def process_image(info, distortion_model):
#--------------------------------------
    # Create row and column tag groups
    row_group = {}
    col_group = {}
    
    for _, taginfo in info.detections.iteritems():
        xy = taginfo.tgt
        xy = distortion_model.undistort(*xy)

        rid = taginfo.row
        if rid in row_group.keys():
            row_group[rid].append(xy)
        else: row_group[rid] = [xy]  
        
        cid = taginfo.col
        if cid in col_group.keys():
            col_group[cid].append(xy)
        else: col_group[cid] = [xy]
        
    # Find max_abserr and mean_abserr over all groups
    mean_abserr = []; max_abserr = []

    # The best of x-vs-y or y-vs-x
    def best_regress(x, y):
        p1 = np.polyfit(x, y, 1)
        abserr1 = np.fabs(y - np.polyval(p1, x))
        p2 = np.polyfit(y, x, 1)
        abserr2 = np.fabs(x - np.polyval(p2, y))
        return abserr1 if np.amax(abserr1) < np.amax(abserr2) else abserr2

    for group in row_group, col_group:
        for _, grp in group.iteritems():
            if len(grp) > 3:
                pts = np.array(grp)
                residuals = best_regress(pts[:, 0], pts[:, 1])
                mean_abserr.append(np.mean(residuals))
                max_abserr.append(np.amax(residuals))
                
    return np.mean(mean_abserr), np.amax(max_abserr)
            

if __name__ == "__main__":
#--------------------------------------
    polymodel = PolyUndistortionModel(sys.argv[1])
    gpmodel = GPUndistortionModel(sys.argv[1])
    
    result = {}
    
    for name, info in jsonx.load_file(sys.argv[2]).iteritems():
        result[name] = {}        
    
        for type, distortion_model in [('poly', polymodel), ('gp', gpmodel)]:
            mean_abserr, max_abserr = process_image(info, distortion_model)
            result[name][type] = dict(mean_abserr=mean_abserr, max_abserr=max_abserr)
            
    jsonx.dump(result, sys.stdout)