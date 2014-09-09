local-homography
================

Paper
----
The paper decsribing this method is available at http://april.eecs.umich.edu/papers/details.php?name=ranganathan2014iros

Datasets used in the research publication are checked into the repository as `datasets.tar.gz`


Code organization
----
This code is for locally weighted homography estimation and non-parameteric lens
distortion correction.

The code is organized as a bunch of python/jython scripts invoking java code to
perform distortion correction on a tag-mosaic image. The evaluation scripts
operate on a tag-mosaic image directory to compare the classic camera calibration
method with the augmented-method using the non-parametric lens distortion.

This set of scripts has a dependency on the april robotics toolkit java library:
http://april.eecs.umich.edu/wiki/.

Most of the useful code lives in `jython/estim` with adhoc evaluation scripts in
`jython/eval`. Each script performs some calculation and spills its guts into a
JSON output file. Subsequent scripts read from these JSON files and do further
processing.


Script Pipeline
----

This is the rough sequence for the pipeline of estimation scripts:

(A) Start with straightness evaluation on undistorted image

1. Obtain tag training correspondences              > (corrs0.json)
2. Obtain tag testing correspondences               > (corrs1.json)
3. Estimate local homography at center              > (homographies0.json)
4. Estimate GP/poly undistortion model              > (undistortion_model.json)
5. Estimate Gaussian process undistortion table     > (gptable.json)
6. Evaluate straightness                            > (straightness.json)

(B) Classic vs. Augmented calibration comparison

1. Obtain tag training correspondences              > (corrs1.json)
2. Obtain tag testing correspondences               > (corrst.json)
3. Initial intrinsics estimate                      > (intrinsics_d.json)
4. Classic camera calibration                       > (calib_classic.json)
5. Non-parametric undistort correspondences         > (ucorrs1.json)
6. Initial intrinsics estimate (after undistortion) > (intrinsics.json)
7. Non-parametric undistort test correspondences    > (ucorrst.json)
8. Monte-carlo sample from undistortion model       > (mc_urcorrs1.json)
9. Augmented camera calibration                     > (calib_augmented.json)
10. Calibration convergence comparison              > (calib_convergence.json)
