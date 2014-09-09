#!/usr/bin/python

'''
    USAGE: make_data_folds DIRLIST...
'''

import sys
import os, os.path
from glob import glob
import random


if __name__ == '__main__':
#--------------------------------------
    basedir = sys.argv[1]
    pngfiles = glob(os.path.join(basedir, '*.png'))
    
    for fold in ('fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold0'):
        foldpath = os.path.join(basedir, fold)

        # Make a clean directory for fold
        if not os.path.isdir(foldpath):
            os.mkdir(foldpath)
        else:
            for f in glob(os.path.join(foldpath, '*')):
                os.unlink(f)
            
        random.shuffle(pngfiles)
        
        for i, png in zip(range(len(pngfiles)-3), pngfiles[:-3]):
            name = 'im1%02d.png' % i
            os.link(png, os.path.join(foldpath, name))
        
        for i, png in zip(range(3), pngfiles[-3:]):
            name = 't%03d.png' % i
            os.link(png, os.path.join(foldpath, name))
            
        os.link(os.path.join(basedir,'undistortion_model.json'),
                os.path.join(foldpath,'undistortion_model.json'))
