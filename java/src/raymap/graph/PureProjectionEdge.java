package raymap.graph;

import java.io.*;
import java.util.*;

import april.graph.*;
import april.jmat.*;
import april.util.*;


public class PureProjectionEdge extends GEdge
{
    /* each correspondence is: worldx, worldy, imagex, imagey */
    public ArrayList<double[]> correspondences;
    public String name;

    public PureProjectionEdge(ArrayList<double[]> correspondences, String name)
    {
        this.nodes = new int[] { -1, -1 }; // make sure someone sets us later.
        this.correspondences = correspondences;
        this.name = name;
    }

    public int getDOF()
    {
        return correspondences.size();
    }

    public double getChi2(Graph g)
    {
        double err2 = 0;
        for (double corr[] : correspondences) {
            err2 += LinAlg.sq(getResidual(g, corr));
        }

        return err2;
    }

    public double getResidual(Graph g, double corr[])
    {
        IntrinsicsNode in = (IntrinsicsNode) g.nodes.get(nodes[0]);
        ExtrinsicsNode ex = (ExtrinsicsNode) g.nodes.get(nodes[1]);

        double[] world = new double[] { corr[0], corr[1] };
        double[] image = PerspectiveProjection.worldToImage(in, ex, world);

        return LinAlg.distance(image, new double[] {corr[2], corr[3]}, 2);
    }

    public Linearization linearize(Graph g, Linearization lin)
    {
        if (lin == null) {
            lin = new Linearization();

            for (int nidx = 0; nidx < nodes.length; nidx++) {
                lin.J.add(new double[correspondences.size()][g.nodes.get(nodes[nidx]).state.length]);
            }

            lin.R = new double[correspondences.size()];
            lin.W = LinAlg.identity(correspondences.size());

            // chi2 is sum of error of each correspondence, so W
            // should just be 1.
        }

        for (int cidx = 0; cidx < correspondences.size(); cidx++) {
            lin.R[cidx] = getResidual(g, correspondences.get(cidx));

            for (int nidx = 0; nidx < nodes.length; nidx++) {
                GNode gn = g.nodes.get(nodes[nidx]);

                double s[] = LinAlg.copy(gn.state);
                for (int i = 0; i < gn.state.length; i++) {

                    double eps = Math.max(0.001, Math.abs(gn.state[i]) / 1000);

                    gn.state[i] = s[i] + eps;
                    double chiplus = LinAlg.sq(getResidual(g, correspondences.get(cidx)));

                    gn.state[i] = s[i] - eps;
                    double chiminus = LinAlg.sq(getResidual(g, correspondences.get(cidx)));

                    lin.J.get(nidx)[cidx][i] = (chiplus - chiminus) / (2*eps);

                    gn.state[i] = s[i];
                }
            }
        }

        return lin;
    }

    public PureProjectionEdge copy()
    {
        throw new RuntimeException("Not Implemented!");
    }

    public void write(StructureWriter outs) throws IOException
    {
        throw new RuntimeException("Not Implemented!");
    }

    public void read(StructureReader ins) throws IOException
    {
        throw new RuntimeException("Not Implemented!");
    }
}
