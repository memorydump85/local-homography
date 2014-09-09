package raymap.graph;

import java.util.*;

import april.graph.*;
import april.jmat.*;


public class ProjectionTestEdge extends ProjectionEdge
{
    public ProjectionTestEdge(ArrayList<double[]> correspondences, String name)
    {
        super(correspondences, name);
    }

    public double getResidual(Graph g, double corr[])
    {
        IntrinsicsNode in = (IntrinsicsNode) g.nodes.get(0);
        ExtrinsicsNode ex = (ExtrinsicsNode) g.nodes.get(nodes[0]);
        IDistortionNode distort = (IDistortionNode) g.nodes.get(1);

        double[] world = new double[] { corr[0], corr[1] };
        double[] image = PerspectiveProjection.worldToImage(in, ex, world);
        image = distort.apply(image, in.state[2], in.state[3]);

        return LinAlg.distance(image, new double[] {corr[2], corr[3]}, 2);
    }
}
