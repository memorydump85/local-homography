package raymap.graph;

import april.graph.*;
import april.jmat.*;


public class ExtrinsicsNode extends GNode
{
    /** state:
      * 0-2: xyz
      * 3-5: rpy
      */

    public ExtrinsicsNode(double[] xyzrpy)
    {
        this.state = LinAlg.copy(xyzrpy);
        this.init = LinAlg.copy(xyzrpy);
    }

    public int getDOF()
    {
        assert(state.length==6);
        return state.length; // should be 6
    }

    public ExtrinsicsNode copy()
    {
        throw new RuntimeException("Not implemented!");
    }

    public double[] toXyzRpy(double[] s)
    {
        throw new RuntimeException("Not implemented!");
    }
}
