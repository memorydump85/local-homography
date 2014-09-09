#!/usr/bin/python
'''
	USAGE: ./gen_reports.sh DIRLIST...
'''

import sys
import os
from os.path import join
from glob import glob
from util import jsonx
from sys import stdout


if __name__ == '__main__':
#--------------------------------------
	print ' Straightness results '
	print '----------------------'

	for dataset in sys.argv[1:]:		
		jsonfile = join(dataset, 'straightness.json')
		if not os.path.isfile(jsonfile): continue
		
		print dataset + '(mean_abserr, max_abserr)'
		json = jsonx.load_file(jsonfile)

		stdout.write('  POLY: ')
		for im, info in json.iteritems():
			stdout.write('%0.2f %0.2f   ' % (info.poly.mean_abserr, info.poly.max_abserr))
		print

		stdout.write('    GP: ')
		for im, info in json.iteritems():
			stdout.write('%0.2f %0.2f   ' % (info.gp.mean_abserr, info.gp.max_abserr))
		print
		print


	print ' Cross-validation results (training) '
	print '-------------------------------------'
	
	for dataset in sys.argv[1:]:
		folds = glob(join(dataset, 'fold*'))
		if len(folds) == 0: continue
		
		print dataset + ' (rmse, max)'

		stdout.write('  classic: ')
		for fold in folds:
			r = jsonx.load_file(join(fold, 'calib_classic.json'))
			stdout.write("%.2f %.2f   " % (r.rmse, r.maxerr))
		print

		stdout.write('augmented: ')
		for fold in folds:
			r = jsonx.load_file(join(fold, 'calib_augmented.json'))
			stdout.write("%.2f %.2f   " % (r.rmse, r.maxerr))
		print '\n'
			
	
	print ' Cross-validation results (validation) '
	print '---------------------------------------'
	
	for dataset in sys.argv[1:]:
		folds = glob(join(dataset, 'fold*'))
		if len(folds) == 0: continue
		
		print dataset + ' (rmse, max)'

		stdout.write('  classic: ')
		for fold in folds:
			r = jsonx.load_file(join(fold, 'calib_classic.json'))
			stdout.write("%.2f %.2f   " % (r.test_rmse, r.test_maxerr))
		print

		stdout.write('augmented: ')
		for fold in folds:
			r = jsonx.load_file(join(fold, 'calib_augmented.json'))
			stdout.write("%.2f %.2f   " % (r.test_rmse, r.test_maxerr))
		print '\n'
