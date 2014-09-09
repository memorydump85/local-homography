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

public class LocalInvHomographyTest
{
    static TagFamily tf = new Tag36h11();
    static TagDetector td = new TagDetector(tf);

    public static void main(String[] args) throws IOException
    {
        final BufferedImage im = ImageIO.read(new File(args[0]));
        final ArrayList<TagDetection> detections =
            td.process(im, new double[] {im.getWidth()/2.0, im.getHeight()/2.0});

        WeightedLocalHomography wh = new WeightedLocalHomography(
                new SqExpWeightingFunction(50));

        int i = 0;
        for (TagDetection d : detections) {
            double[] wxy = OriginalMosaic.getPosition(d.id);
            wh.addCorrespondence(d.cxy, wxy);
            System.out.printf("%.2f %.2f - %.2f %.2f\n",
                    d.cxy[0], d.cxy[1],
                    wxy[0], wxy[1]);
        }

        double[] qi = wh.map(new double[] {376.00, 240.00, 1});
        LinAlg.scaleEquals(qi, 1.0/qi[2]);
        LinAlg.printTranspose(qi);

        JFrame jf = new JFrame();
        jf.setTitle("Local Inverse Homography Test");
        jf.setLayout(new BorderLayout());

        VisWorld vw = new VisWorld();
        VisLayer vl = new VisLayer(vw);
        VisCanvas vc = new VisCanvas(vl);

        vc.setBackground(Color.black);
        jf.add(vc, BorderLayout.CENTER);

        ParameterGUI pg = new ParameterGUI();
        pg.addDouble("tau", "smoothing", 50);
        pg.addDouble("lambda", "regularizer", 0);
        jf.add(pg, BorderLayout.SOUTH);

        jf.setSize(800, 800);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jf.setVisible(true);

        final VisWorld.Buffer vbi = vw.getBuffer("img");
        vbi.addBack(new VzImage(new FloatImage(im).scale(0.25).makeImage()));
        vbi.swap();

        final VisWorld.Buffer vb = vw.getBuffer("content");
        pg.addListener(new ParameterListener() {
            public void parameterChanged(final ParameterGUI pg, String name)
            {
                for (int y=0; y<480; y+=20) {
                    VisVertexData vvd = new VisVertexData();
                    VisVertexData vvc = new VisVertexData();

                    for (int x=0; x<752; x+=20) {
                        double[] q = {x, y};
                        final double tau = pg.gd("tau");
                        final double lambda = pg.gd("lambda");

                        WeightedLocalHomography wh = new WeightedLocalHomography(
                                new SqExpWeightingFunction(tau));
                        wh.setRegularization(lambda);

                        int i = 0;
                        for (TagDetection d : detections) {
                            wh.addCorrespondence(d.cxy, OriginalMosaic.getPosition(d.id));
                            vvc.add(new double[] {d.cxy[0], d.cxy[1], 3});
                        }

                        double[] qi = wh.map(new double[] {q[0], q[1], 1});
                        LinAlg.scaleEquals(qi, 1.0/qi[2]);
                        LinAlg.printTranspose(qi);
                        vvd.add(qi);
                    }

                    vb.addBack(new VzLines(vvd, VzLines.LINE_STRIP, new VzLines.Style(Color.red, 2)));
                    vb.addBack(new VzPoints(vvd, new VzPoints.Style(Color.blue, 2)));
                    vb.addBack(new VzPoints(vvc, new VzPoints.Style(Color.orange, 3)));
                }
                vb.swap();
            }
        });
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
