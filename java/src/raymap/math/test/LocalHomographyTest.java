package raymap.math.test;

import java.awt.*;
import java.awt.image.*;
import java.io.*;
import java.util.*;
import java.util.List;

import javax.imageio.*;
import javax.swing.*;

import april.image.*;
import april.jmat.*;
import april.tag.*;
import april.util.*;
import april.vis.*;

import raymap.math.*;
import raymap.utils.*;

public class LocalHomographyTest
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
        jf.setTitle("Local Homography Test");
        jf.setLayout(new BorderLayout());

        VisWorld vw = new VisWorld();
        VisLayer vl = new VisLayer(vw);
        VisCanvas vc = new VisCanvas(vl);

        vc.setBackground(Color.black);
        jf.add(vc, BorderLayout.CENTER);

        ParameterGUI pg = new ParameterGUI();
        pg.addDouble("tau", "smoothing", 1);
        pg.addDouble("lambda", "regularizer", 0);
        jf.add(pg, BorderLayout.SOUTH);

        jf.setSize(800, 800);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jf.setVisible(true);

        FloatImage fim = new FloatImage(im).normalize();
        fim = sobel(fim);
        fim = invert(fim).normalize();

        final VisWorld.Buffer vbi = vw.getBuffer("img");
        vbi.addBack(new VzImage(fim.makeImage()));
        vbi.swap();

        final VisWorld.Buffer vb = vw.getBuffer("content");
        pg.addListener(new ParameterListener() {
            public void parameterChanged(final ParameterGUI pg, String name)
            {
                for (double[][] line : rowLines) {
                    VisVertexData vvd = new VisVertexData();
                    VisVertexData vvc = new VisVertexData();

                    for (double t=-0.1; t<=1.1; t+=0.01) {
                        double[] q = interpolateLine(line[0], line[1], t);
                        final double tau = pg.gd("tau");
                        final double lambda = pg.gd("lambda");

                        WeightedLocalHomography wh = new WeightedLocalHomography(
                                new SqExpWeightingFunction(tau));
                        wh.setRegularization(lambda);

                        int i = 0;
                        for (TagDetection d : detections) {
                            wh.addCorrespondence(OriginalMosaic.getPosition(d.id), d.cxy);
                            vvc.add(new double[] {d.cxy[0], d.cxy[1], 3});
                        }

                        double[] qi = wh.map(new double[] {q[0], q[1], 1});
                        LinAlg.scaleEquals(qi, 1.0/qi[2]);
                        LinAlg.printTranspose(qi);
                        vvd.add(qi);
                    }

                    vb.addBack(new VzLines(vvd, VzLines.LINE_STRIP, new VzLines.Style(Color.red.darker(), 3)));
                    //vb.addBack(new VzPoints(vvd, new VzPoints.Style(Color.blue, 2)));
                    vb.addBack(new VzPoints(vvc, new VzPoints.Style(Color.black.darker(), 4)));
                }
                vb.swap();
            }
        });
    }

    static FloatImage invert(FloatImage fim)
    {
        fim = fim.normalize();
        for (int i=0; i<fim.d.length; ++i)
            fim.d[i] = (1.0f - fim.d[i]) * 0.25f;

        return fim;
    }

    static FloatImage sobel(FloatImage im)
    {
        float[] ka = LinAlg.normalize(new float[] {1, 2, 1});
        float[] kb = LinAlg.normalize(new float[] {1, 0, -1});

        FloatImage gimx = im.filterFactoredCentered(kb, ka);
        FloatImage gimy = im.filterFactoredCentered(ka, kb);
        FloatImage gim = new FloatImage(im.width, im.height);

        for (int i=0; i<gim.d.length; ++i)
            gim.d[i] = (float) Math.sqrt(gimx.d[i]*gimx.d[i] + gimy.d[i]*gimy.d[i]);

        return gim;
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
