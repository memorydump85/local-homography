package raymap.math;
import java.util.*;

import april.jmat.*;
import april.util.*;


public class WeightedLocalHomography
{
    WeightingFunction wtFunc;
    double regularizationLambda = 0;

    ArrayList<double[]> corrs = new ArrayList<double[]>();
    Normalize2D normSource = new Normalize2D();
    Normalize2D normTarget = new Normalize2D();

    /* the constraint matrix */
    Matrix A;

    public WeightedLocalHomography()
    {
        this.wtFunc = new UnitWeightingFunction();
    }

    public WeightedLocalHomography(WeightingFunction w)
    {
        this.wtFunc = w;
    }

    public void addCorrespondence(double[] source, double[] target)
    {
        addCorrespondence(source[0], source[1], target[0], target[1]);
    }

    public void addCorrespondence(double sourcex, double sourcey, double targetx, double targety)
    {
        corrs.add(new double[] { sourcex, sourcey, targetx, targety });
        normSource.add(sourcex, sourcey);
        normTarget.add(targetx, targety);
        A = null;
    }

    public void setRegularization(double lambda)
    {
        this.regularizationLambda = lambda;
    }

    public void setWeightingFunction(WeightingFunction w)
    {
        this.wtFunc = w;
    }

    public double[] map(double[] srcPt)
    {
        double[][] H = getHomographyAt(srcPt);
        return LinAlg.matrixAB(H, srcPt);
    }

    public double[][] getHomographyAt(double[] srcPt)
    {
        final int N = corrs.size();
        double normSourceT[][] = normSource.getTransform();
        double normTargetT[][] = normTarget.getTransform();

        if (A==null) {

            double[][] A = new double[2*N][];
            for (int c=0; c<N; ++c) {
                double[] corr = corrs.get(c);
                double source[] = LinAlg.transform(normSourceT, LinAlg.copy(corr, 0, 2));
                double target[] = LinAlg.transform(normTargetT, LinAlg.copy(corr, 2, 2));

                double x = source[0], y = source[1];
                double i = target[0], j = target[1];

                A[2*c] = new double[] {-x, -y, -1, 0, 0, 0, i*x, i*y, i};
                A[2*c+1] = new double[] {0, 0, 0, -x, -y, -1, j*x, j*y, j};
            }

            this.A = new Matrix(A);
        }

        double[] w_diag = new double[2*N];
        for (int i=0; i<N; ++i) {
            double[] corr = corrs.get(i);
            double[] a = new double[] {srcPt[0], srcPt[1]};
            double[] b = new double[] {corr[0], corr[1]};
            double w = wtFunc.compute(new double[] {a[0], a[1]}, new double[] {b[0], b[1]});
            w_diag[2*i+1] = w_diag[2*i] = Math.sqrt(w);
        }

        /* Obtain a solution for the weighted constraint matrix using an SVD */
        Matrix lambdaI = Matrix.identity(2*N, 2*N).times(regularizationLambda);
        Matrix W = Matrix.diag(LinAlg.normalizeL1(w_diag)).plus(lambdaI);
        SingularValueDecomposition svd = new SingularValueDecomposition(W.times(A));
        Matrix V = svd.getV();

        double[] h = svd.getV().getColumn(V.getColumnDimension()-1).copyArray();
        /* Rearrange h into a matrix */
        double[][] H = new double[][] {
            {h[0], h[1], h[2]},
            {h[3], h[4], h[5]},
            {h[6], h[7], h[8]}
        };

        H = LinAlg.matrixABC(LinAlg.inverse(normTargetT), H, normSourceT);
        return H;
    }


    public static interface WeightingFunction {
        public double compute(double[] p, double[] q);
    }
}
