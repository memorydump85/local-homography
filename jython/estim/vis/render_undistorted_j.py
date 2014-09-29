from javax.swing import *
from java.awt.image import *
from javax.imageio import *
from java.io import File
from java.lang import Math
from april.jmat import LinAlg
import sys
import util.jsonx as jsonx


#--------------------------------------
class PolyUndistortionModel(object):
#--------------------------------------
    def __init__(self, jsonfile):
        distortion_info = jsonx.load(open(jsonfile))
        self.poly_terms = compile(distortion_info.poly_terms, '', 'eval')
        self.poly_x = distortion_info.poly_x
        self.poly_y = distortion_info.poly_y

            
    def undistort(self, i, j):
        phi = eval(self.poly_terms)
        return (i + LinAlg.dotProduct(phi,self.poly_x), j + LinAlg.dotProduct(phi,self.poly_y))


if __name__ == "__main__":
#--------------------------------------    
    model = PolyUndistortionModel(sys.argv[1])
    im = ImageIO.read(File(sys.argv[2]))

    undistorted = []
    maxx, maxy, minx, miny = float('-Inf'), float('-Inf'), float('Inf'), float('Inf')
    for i in range(im.width):
        for j in range(im.height):
            ii, jj = model.undistort(i, j)
            undistorted.append([ii, jj, im.getRGB(i,j)])
            maxx = Math.max(maxx, ii)
            minx = Math.min(minx, ii)
            maxy = Math.max(maxy, jj)
            miny = Math.min(miny, jj)

    rangex, rangey = maxx-minx, maxy-miny
    imout = BufferedImage(int(im.width*0.4), int(im.height*0.4), BufferedImage.TYPE_INT_ARGB)
    scale = imout.width/rangex

    for u in undistorted:
        x, y = int((u[0]-minx)*scale), int((u[1]-miny)*scale)
        if x < imout.width and y < imout.height:
            imout.setRGB(x, y, 0xFF000000 | u[2])

    token = sys.argv[2].split('.')[0]
    ImageIO.write(imout, 'png', File(token + '.out.png'))