package raymap.graph;

import april.graph.*;
import april.jmat.*;


public class IntrinsicsNode extends GNode
{
    /** state: fx fy cx cy */

    public IntrinsicsNode(double[] state0)
    {
        this.state = LinAlg.copy(state0);
        this.init = LinAlg.copy(state0);
    }

    public int getDOF()
    {
        assert(state.length==4);
        return state.length;
    }

    public IntrinsicsNode copy()
    {
        throw new RuntimeException("Not implemented!");
    }

    public double[] toXyzRpy(double[] s)
    {
        throw new RuntimeException("Not implemented!");
    }
}
