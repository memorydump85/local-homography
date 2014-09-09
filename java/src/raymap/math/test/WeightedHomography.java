package raymap.math.test;

import java.awt.*;
import java.awt.image.*;
import java.io.*;
import java.util.*;
import java.util.List;

import javax.imageio.*;
import javax.swing.*;

import april.jmat.*;
import april.tag.*;
import april.util.*;
import april.vis.*;

import raymap.utils.*;

public class WeightedHomography
{
    static TagFamily tf = new Tag36h11();
    static TagDetector td = new TagDetector(tf);

    public static void main(String[] args) throws IOException
    {
        final BufferedImage im = ImageIO.read(new File(args[0]));
        final ArrayList<TagDetection> detections =
            td.process(im, new double[] {im.getWidth()/2.0, im.getHeight()/2.0});

        final List<double[][]> rowLines = new ArrayList<double[][]>();
        for (int id=0; id<=168; id+=24) {
            double[] a = OriginalMosaic.getPosition(id);
            double[] b = OriginalMosaic.getPosition(id+9);
            rowLines.add(new double[][] {a, b});
        }

        JFrame jf = new JFrame();
        jf.setTitle("Weighted Homography Test");
        jf.setLayout(new BorderLayout());

        VisWorld vw = new VisWorld();
        VisLayer vl = new VisLayer(vw);
        VisCanvas vc = new VisCanvas(vl);

        vc.setBackground(Color.black);
        jf.add(vc, BorderLayout.CENTER);

        ParameterGUI pg = new ParameterGUI();
        pg.addDouble("tau", "smoothing", 1);
        jf.add(pg, BorderLayout.SOUTH);

        jf.setSize(800, 800);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jf.setVisible(true);

        final VisWorld.Buffer vb = vw.getBuffer("content");
        pg.addListener(new ParameterListener() {
            public void parameterChanged(ParameterGUI pg, String name)
            {
                for (double[][] line : rowLines) {
                    VisVertexData vvd = new VisVertexData();
                    VisVertexData vvc = new VisVertexData();

                    for (double t=0; t<=1; t+=0.01) {
                        double[] q = interpolateLine(line[0], line[1], t);
                        double[] w = new double[detections.size()];

                        int i = 0;
                        WeightedHomographySolver solver = new WeightedHomographySolver();
                        for (TagDetection d : detections) {
                            w[i++] = weight(q, OriginalMosaic.getPosition(d.id), pg.gd("tau"));
                            solver.addCorrespondence(OriginalMosaic.getPosition(d.id), d.cxy);
                            vvc.add(new double[] {d.cxy[0], d.cxy[1], 2});
                        }

                        double[][] H = solver.solve(LinAlg.normalize(w));
                        double[] qi = LinAlg.matrixAB(H, new double[] {q[0], q[1], 1});
                        LinAlg.scaleEquals(qi, 1.0/qi[2]);

                        vvd.add(qi);
                    }

                    vb.addBack(new VzLines(vvd, VzLines.LINE_STRIP, new VzLines.Style(Color.blue, 1)));
                    vb.addBack(new VzPoints(vvd, new VzPoints.Style(Color.cyan, 2)));
                    vb.addBack(new VzPoints(vvc, new VzPoints.Style(Color.orange, 3)));
                }
                vb.swap();
            }
        });

        final VisWorld.Buffer vbi = vw.getBuffer("img");
        vbi.addBack(new VzImage(im));
        vbi.swap();
    }

    static double[] interpolateLine(double[] a, double[] b, double t)
    {
        double[] d = LinAlg.subtract(b, a);
        return LinAlg.add(a, LinAlg.scale(d, t));
    }

    static double weight(double[] p, double[] q, double t)
    {
        double[][] cov = LinAlg.diag(new double[] {t, t});
        return new MultiGaussian(cov, p).prob(q);
    }
}

class WeightedHomographySolver
{
    ArrayList<double[]> constraint = new ArrayList<double[]>();

    public void addCorrespondence(double[] image, double[] world)
    {
        double i = image[0], j = image[1];
        double x = world[0], y = world[1];

        constraint.add(new double[] {-i, -j, -1, 0, 0, 0, x*i, x*j, x});
        constraint.add(new double[] {0, 0, 0, -i, -j, -1, y*i, y*j, y});
    }

    double[][] solve()
    {
        return solve(null);
    }

    double[][] solve(double[] weights)
    {
        if (weights != null) {
            /* two constraints for each correspondence.
             * Hence double the weight values */
            double[] w = new double[weights.length*2];
            for (int i=0; i<weights.length; ++i)
                w[2*i] = w[2*i+1] = weights[i];

            weights = w;
        }

        final int N = constraint.size();
        final int M = constraint.get(0).length;

        Matrix A = new Matrix(N, M);
        for (int i=0; i<N; ++i) {
            A.setRow(i, new DenseVec(constraint.get(i)));
        }

        Matrix W = (weights == null) ? Matrix.identity(N, N) : Matrix.diag(weights);
        SingularValueDecomposition svd = new SingularValueDecomposition(W.times(A));
        Matrix V = svd.getV();

        double[] h = V.getColumn(V.getColumnDimension()-1).copyArray();
        LinAlg.printTranspose(h);
        final double[][] H = new double[][] {
                { h[0],  h[1],  h[2] },
                { h[3],  h[4],  h[5] },
                { h[6],  h[7],  h[8] },
        };
        return H;
    }
}
