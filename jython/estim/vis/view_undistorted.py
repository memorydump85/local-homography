from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import array
import numpy as np
import sys
from estim.undistortion_model import *
from util import jsonx

ESCAPE = '\033'

window = 0
texture = 0
im = None
fwd_map = None


def LoadTextures(texture_file):
    global im
    im = Image.open(texture_file)


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    global im
    pixels_rgba = im.convert("RGBA").tostring("raw", "RGBA")

    ix = im.size[0]
    iy = im.size[1]

    # Create Texture    
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))   # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels_rgba)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glEnable(GL_TEXTURE_2D)
    
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(25.0, float(Width)/float(Height), 0.1, 10000.0)
    glMatrixMode(GL_MODELVIEW)


def compute_fwd_map(jsonfile):
    W, H = im.size[0], im.size[1]
    
    global fwd_map
    
    if False:
        print "Computing Forward Map ..."
        model = PolyUndistortionModel(jsonfile)
        distorted_pixels = dict( ((i,j), model.undistort(i,j)) \
                                    for i in range(0, W) for j in range(0, H) )
        fwd_map = distorted_pixels
    else:
        print "Loading Forward Map ..."
        fwd_map = {}
        json = jsonx.load_file(jsonfile)
        for from_repr, to in json.iteritems():
            fwd_map[eval(from_repr)] = to
    
    print "\nDone."


# The main drawing function. 
vx = []
tx = []

def DrawGLScene():
    global texture
    global im
    global vx
    global tx

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    glLoadIdentity()                    # Reset The View
    glTranslatef(-200.,100.,-3000.0)            # Move Into The Screen

    glRotatef(0,  1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
    glRotatef(180,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
    glRotatef(180,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis

    if len(vx)==0:
        print 'Computing Vertex Array ...'

        W, H = float(im.size[0]), float(im.size[1])
        print W, H
        normalize = lambda x, y: (x/W, y/H)

        for i in range(0, im.size[0]-1):
            for j in range(0, im.size[1]-1):
                tx.append(normalize(i, j)); vx.append(fwd_map[(i, j)])
                tx.append(normalize(i+1, j)); vx.append(fwd_map[(i+1, j)])
                tx.append(normalize(i+1, j+1)); vx.append(fwd_map[(i+1, j+1)])
                tx.append(normalize(i, j+1)); vx.append(fwd_map[(i, j+1)])

        print 'Done.'

    glBegin(GL_QUADS)

    for i in range(0, len(vx)):
        glTexCoord2d(*tx[i]);
        glVertex2d(*vx[i])
    
    glEnd();
    glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        sys.exit()


def main():
    LoadTextures(sys.argv[2])
    compute_fwd_map(sys.argv[1])

    global window
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    # get a 320 x 240 window 
    glutInitWindowSize(640, 480)
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(0, 0)
    
    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Undistorted: " + sys.argv[2])

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    
    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    #glutIdleFunc(DrawGLScene)
    
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyPressed)

    # Initialize our window. 
    InitGL(640, 480)

    # Start Event Processing Engine    
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
