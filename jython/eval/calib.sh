#!/bin/bash

export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/jython
export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/java/raymap.jar
export PYTHONPATH=$PYTHONPATH:/home/rpradeep/studio/raymap/jython

DIR=$1


echo '  [A] Extracting correspondences ...'
$JYTHON ../estim/correspondences.j.py $DIR/im1*.png > $DIR/corrs1.json

echo '  [A] Extracting test correspondences ...'
$JYTHON ../estim/correspondences.j.py $DIR/t*.png > $DIR/corrst.json

echo '  [A] Estimating intrinsics from distorted points...'
$JYTHON ../estim/estimate_intrinsics.j.py $DIR/corrs1.json > $DIR/intrinsics_d.json

echo '  [A] Classic camera calibration ...'
$JYTHON calib_classic_j.py \
	--correspondences $DIR/corrs1.json \
	--intrinsics $DIR/intrinsics_d.json \
	--test $DIR/corrst.json \
		> $DIR/calib_classic.json


echo '  [B] Undistorting correspondences ...'
python ../estim/undistort_correspondences.py $DIR/corrs1.json $DIR/undistortion_model.json > $DIR/ucorrs1.json

echo '  [B] Estimating intrinsics from undistorted points...'
$JYTHON ../estim/estimate_intrinsics.j.py $DIR/ucorrs1.json > $DIR/intrinsics.json

echo '  [B] Undistorting test correspondences ...'
python ../estim/undistort_correspondences.py $DIR/corrst.json $DIR/undistortion_model.json > $DIR/ucorrst.json

echo '  [B] Sampling undistortion ...'
python ../estim/montecarlo_undistort_correspondences.py $DIR/corrs1.json $DIR/undistortion_model.json > $DIR/mc_ucorrs1.json

echo '  [B] Augmented camera calibration ...'
$JYTHON calib_augmented_j.py \
	--correspondences $DIR/mc_ucorrs1.json \
	--intrinsics $DIR/intrinsics.json \
	--test $DIR/ucorrst.json \
		> $DIR/calib_augmented.json


if [ -e $DIR/homographies0.json -a ! -e $DIR/calib_convergence.json ]; then
	echo ' '
	echo '  Convergence comparison ...'
	$JYTHON calib_convergence_j.py \
		--correspondences $DIR/corrs1.json \
		--test $DIR/corrst.json \
		--ucorrespondences $DIR/mc_ucorrs1.json \
		--utest $DIR/ucorrst.json \
			> $DIR/calib_convergence.json
fi


echo '  Done.'