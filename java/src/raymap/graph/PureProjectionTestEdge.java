package raymap.graph;

import java.util.*;

import april.graph.*;
import april.jmat.*;


public class PureProjectionTestEdge extends PureProjectionEdge
{
    public PureProjectionTestEdge(ArrayList<double[]> correspondences, String name)
    {
        super(correspondences, name);
    }

    public double getResidual(Graph g, double corr[])
    {
        IntrinsicsNode in = (IntrinsicsNode) g.nodes.get(0);
        ExtrinsicsNode ex = (ExtrinsicsNode) g.nodes.get(nodes[0]);

        double[] world = new double[] { corr[0], corr[1] };
        double[] image = PerspectiveProjection.worldToImage(in, ex, world);

        return LinAlg.distance(image, new double[] {corr[2], corr[3]}, 2);
    }
}
