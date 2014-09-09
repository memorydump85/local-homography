import sys
import optparse
import util.jsonx as jsonx
from array import  array

from java.util import ArrayList
from april.tag import CameraUtil
from april.image import Homography33b
from april.graph import Graph, LMSolver
from raymap.graph import IntrinsicsNode, ExtrinsicsNode, RadialDistortionNode, ProjectionEdge, ProjectionTestEdge
from april.jmat import LinAlg
from april.jmat.ordering import MinimumDegreeOrdering


def complete_graph(g, json, EdgeClass, selectf):
#--------------------------------------
#    assume g.nodes[0] = intrinsics, g.nodes[1] = distortion
 
    inode = g.nodes.get(0)
     
    for name, info in json.iteritems():
        if len(info.detections) < 8: continue
        corrs = [ array('d', corr.src + corr.tgt) for _, corr in info.detections.iteritems() ]
         
        h = Homography33b()
        for c in corrs: h.addCorrespondence(*c)
         
        fx, fy, cx, cy = inode.state
        pose = CameraUtil.homographyToPose(-fx, fy, cx, cy, h.getH())
        extrinsics = ExtrinsicsNode(LinAlg.matrixToXyzrpy(pose))
         
        exidx = g.nodes.size()
        g.nodes.add(extrinsics)
         
        edge = EdgeClass(ArrayList(corrs), name)
        edge.nodes = selectf([0, 1, exidx])
        g.edges.add(edge)

        
def rmse(g):
#--------------------------------------    
    sse, n = 0, 0
    for e in filter(lambda x: isinstance(x, ProjectionEdge), g.edges):
        sse += e.getChi2(g)
        n += e.getDOF();
    return sse/n


def maxerr(g):
#--------------------------------------
    maxerr = 0
       
    for e in filter(lambda x: isinstance(x, ProjectionEdge), g.edges):
        for c in e.correspondences:
            maxerr = max(maxerr, e.getResidual(g, c))
    return maxerr


def calibrate(intrinsics, tag_correspondences, test_correspondences):
#--------------------------------------
#   All parameters are JSON dictionary objects
    
    inode = IntrinsicsNode([intrinsics.fx, intrinsics.fy, intrinsics.cx, intrinsics.cy])
    dnode = RadialDistortionNode([0, 0, 0, 0, 0, 0])
    LMSolver.verbose = False
    

    # construct graph and optimize
    g = Graph()
    g.nodes.add(inode); g.nodes.add(dnode)
    complete_graph(g, tag_correspondences, ProjectionEdge, lambda x : x)
    
    solver = LMSolver(g, MinimumDegreeOrdering(), 10e-6, 10e6, 2)
    for _ in xrange(0, 10000):
        if not solver.canIterate(): break
        solver.iterate()

    # construct test graph and optimize
    gtest = Graph()
    gtest.nodes.add(inode); gtest.nodes.add(dnode)
    complete_graph(gtest, test_correspondences, ProjectionTestEdge, lambda x : [x[2]])
 
    solver = LMSolver(gtest, MinimumDegreeOrdering(), 10e-6, 10e6, 2)
    for _ in xrange(0, 10000):
        if not solver.canIterate(): break
        solver.iterate()
        
    # dump results
    result = dict(intrinsics=list(inode.state),
                  rmse=rmse(g), test_rmse=rmse(gtest),
                  maxerr=maxerr(g), test_maxerr=maxerr(gtest))
        
    if False:
        for e in filter(lambda x: isinstance(x, ProjectionEdge), g.edges):
            ex = g.nodes.get(e.nodes[2])
            result[e.name] = list(ex.state)

    return result


if __name__ == '__main__':
#--------------------------------------
    optparser = optparse.OptionParser()
    optparser.add_option('--correspondences',
                         action='store', type='string', dest='tagfile',
                         help='JSON data-file containing tag correspondences for an image set')
    optparser.add_option('--intrinsics',
                         action='store', type='string', dest='ifile',
                         help='JSON data-file containing camera intrinsic estimates')
    optparser.add_option('--test',
                         action='store', type='string', dest='testfile',
                         help='JSON data-file containing test image set camera intrinsic estimates')
    
    opts, _ = optparser.parse_args()
    tag_correspondences = jsonx.load(open(opts.tagfile))
    test_correspondences = jsonx.load(open(opts.testfile))
    K = jsonx.load(open(opts.ifile))

    result = calibrate(K, tag_correspondences, test_correspondences)        
    jsonx.dump(result, sys.stdout)
