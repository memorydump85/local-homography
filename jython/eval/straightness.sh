#!/bin/bash

export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/jython
export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/java/raymap.jar
export PYTHONPATH=$PYTHONPATH:/home/rpradeep/studio/raymap/jython

DIR=$1

echo '  Extracting distortion correspondences ...'
$JYTHON ../estim/correspondences.j.py $DIR/im0*.png > $DIR/corrs0.json

echo '  Extracting other correspondences ...'
$JYTHON ../estim/correspondences.j.py $DIR/im1*.png > $DIR/corrs1.json

echo '  Determining local homographies ...'
$JYTHON ../estim/estimate_homography.j.py $DIR/corrs0.json > $DIR/homographies0.json

echo '  Computing undistortion model ...'
python ../estim/estimate_undistortion.py --correspondences $DIR/corrs0.json --homographies $DIR/homographies0.json --init $DIR/model_init.json > $DIR/undistortion_model.json

echo '  Computing GP undistortion table ...'
python gp_undistortion_table.py $DIR/undistortion_model.json $DIR/corrs0.json > $DIR/gptable.json

echo '  Straightness Evaluation ...'
python straightness.py $DIR/undistortion_model.json $DIR/corrs1.json > $DIR/straightness.json

echo '  Done.'