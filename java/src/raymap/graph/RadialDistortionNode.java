package raymap.graph;

import april.graph.*;
import april.jmat.*;


public class RadialDistortionNode extends GNode implements IDistortionNode
{
    public RadialDistortionNode(double[] poly)
    {
        this.state = LinAlg.copy(poly);
        this.init = LinAlg.copy(poly);
    }

    public int getDOF()
    {
        return state.length;
    }

    public RadialDistortionNode copy()
    {
        throw new RuntimeException("Not implemented!");
    }

    public double[] toXyzRpy(double[] s)
    {
        throw new RuntimeException("Not implemented!");
    }

    @Override
    public double[] apply(double[] p, double cx, double cy)
    {
        double dx = p[0] - cx;
        double dy = p[1] - cy;

        double r = Math.sqrt(dx*dx + dy*dy);
        double theta = Math.atan2(dy, dx);

        double rp = r + eval(r);

        return new double[] { Math.cos(theta)*rp + cx, Math.sin(theta)*rp + cy };
    }

    public double eval(double r)
    {
        double v = 0;
        double p = r;
        for (int i=0; i<state.length; ++i) {
            v += state[i]*p;
            p *= r;
        }

        return v;
    }
}
