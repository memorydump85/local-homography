import sys
import optparse
import util.jsonx as jsonx
from util.jsonx import DotDict
from  calib_classic_j import calibrate as calibrate_classic
from calib_augmented_j import calibrate as calibrate_augmented


if __name__ == '__main__':
#--------------------------------------
    optparser = optparse.OptionParser()
    optparser.add_option('--correspondences',
                         action='store', type='string', dest='tagfile',
                         help='JSON data-file containing tag correspondences for an image set')
    optparser.add_option('--ucorrespondences',
                         action='store', type='string', dest='utagfile',
                         help='JSON data-file containing undistorted tag correspondences for an image set')
    optparser.add_option('--test',
                         action='store', type='string', dest='testfile',
                         help='JSON data-file containing test image set camera intrinsic estimates')
    optparser.add_option('--utest',
                         action='store', type='string', dest='utestfile',
                         help='JSON data-file containing undistorted test image set camera intrinsic estimates')
    
    opts, _ = optparser.parse_args()
    tag_correspondences = jsonx.load(open(opts.tagfile))
    test_correspondences = jsonx.load(open(opts.testfile))
    utag_correspondences = jsonx.load(open(opts.utagfile))
    utest_correspondences = jsonx.load(open(opts.utestfile))
    
    W, H = tag_correspondences.iteritems().next()[1].size
    cx, cy = W/2., H/2.

    results = {}
    for fx in xrange(200, 600, 40):
        for fy in xrange(200, 600, 40):
            intrinsics = DotDict(dict(fx=fx, fy=fy, cx=cx, cy=cy))
            key = '%d,%d' % (fx,fy)
            
            try: a = calibrate_classic(intrinsics, tag_correspondences, test_correspondences)
            except: a = dict(intrinsics = [])
                
            try: b = calibrate_augmented(intrinsics, utag_correspondences, utest_correspondences)
            except: b = dict(intrinsics = [])

            results[key] = dict(classic=a['intrinsics'], augmented=b['intrinsics'])
            
            sys.stderr.write('    "%s": {\n' % key)
            sys.stderr.write('      %s,\n' % str(a['intrinsics']))
            sys.stderr.write('      %s\n' % str(b['intrinsics']))
            sys.stderr.write('    },\n')
            
    jsonx.dump(results, sys.stdout)