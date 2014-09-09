package raymap.graph;

import april.jmat.*;


public class PerspectiveProjection
{
    public static double[] worldToImage(IntrinsicsNode in, ExtrinsicsNode ex, double[] p)
    {
        return projectIntrinsic(in, projectExtrinsic(ex, p));
    }

    static double[] projectExtrinsic(ExtrinsicsNode gex, double[] p)
    {
        double[][] M = LinAlg.xyzrpyToMatrix(gex.state);
        return LinAlg.matrixAB(M, new double[] { p[0], p[1], 0, 1 });
    }

    static double[] projectIntrinsic(IntrinsicsNode in, double[] p)
    {
        assert(p.length==4); /* 3D homogeneous coordinates in, please */

        double[] v = in.state;
        double M[][] = new double[][] { { -v[0],    0,  v[2],  0 },
                                        {     0, v[1],  v[3],  0 },
                                        {     0,    0,     1,  0 } };
        double q[] = LinAlg.matrixAB(M, p);
        q[0] /= q[2];
        q[1] /= q[2];
        q[2] = 1;

        return q;
    }
}
