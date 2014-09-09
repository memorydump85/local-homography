'''
    USAGE: jython correspondences.jy list-of-tag-mosaic-images
'''


from april.tag import *
from java.awt import *
from javax.imageio import *
from java.io import File
import sys.stdout
import simplejson


tf = Tag36h11()
td = TagDetector(tf)
mosaic = TagMosaic(tf, 0.0254)


if __name__ == "__main__":
#--------------------------------------
    files = sys.argv[1:]
    
    image_info = {}
    cxy = None
    
    for imfile in files:
        im = ImageIO.read(File(imfile))
        
        if (cxy is not None) and (cxy != [im.width/2., im.height/2.]):
            sys.stderr.write('ERROR: All images must be of the same size!\n')
            sys.stderr.flush()
            sys.exit(-1)
        
        cxy = [im.width/2., im.height/2.]
        
        dets = {}
        for d in td.process(im, cxy):
            s = mosaic.getPositionMeters(d.id)
            t = d.cxy
            dets[d.id] = dict(
                              src=(round(s[0], 4), round(s[1], 4)),
                              tgt=(round(t[0], 4), round(t[1], 4)),
                              row=mosaic.getRow(d.id),
                              col=mosaic.getColumn(d.id)
                              )
        
        image_info[imfile] = dict(size=[im.width, im.height], detections=dets)

    simplejson.dump(image_info, sys.stdout, sort_keys=True, indent=2)
