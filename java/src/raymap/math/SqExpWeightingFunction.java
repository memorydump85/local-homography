package raymap.math;

import april.jmat.*;

import raymap.math.WeightedLocalHomography.*;

public class SqExpWeightingFunction implements WeightingFunction {
    public final double tau;
    MultiGaussian mg;

    public SqExpWeightingFunction(double bandwidth) {
        this.tau = bandwidth;
        double[][] cov = LinAlg.diag(new double[] {tau, tau});
        this.mg = new MultiGaussian(cov);
    }

    @Override
    public double compute(double[] p, double[] q) {
        return mg.prob(LinAlg.subtract(q, p));
    }
}