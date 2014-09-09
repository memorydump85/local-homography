package raymap.math;

import raymap.math.WeightedLocalHomography.WeightingFunction;


public class UnitWeightingFunction implements WeightingFunction {
    @Override
    public double compute(double[] p, double[] q) {
        return 1;
    }
}