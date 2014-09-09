#!/bin/bash

export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/jython
export CLASSPATH=$CLASSPATH:/home/rpradeep/studio/raymap/java/raymap.jar
export PYTHONPATH=$PYTHONPATH:/home/rpradeep/studio/raymap/jython

DIR=$1


./straightness.sh $DIR

./calib.sh $DIR

echo '  Cross-validation over data folds ...'
python make_data_folds.py $DIR
parallel /bin/bash calib.sh ::: $DIR/fold*

echo '--------------------------------'
echo ' '
echo ' '