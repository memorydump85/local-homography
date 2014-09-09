package raymap.math.test;

import java.awt.*;
import java.awt.image.*;
import java.io.*;
import java.util.*;

import javax.imageio.*;
import javax.swing.*;

import raymap.utils.*;
import raymap.utils.TagSetExtractor.*;

import april.jmat.*;
import april.tag.*;
import april.vis.VisCameraManager.CameraPosition;
import april.vis.*;


public class LiftedHomography
{

    public static void main(String[] args) throws IOException
    {
        final BufferedImage im = ImageIO.read(new File(args[0]));
        TagSet sets = TagSetExtractor.getTagSets(im);

        double[][] Hsmall = null;
        if (true){
            LiftedHomographySolver solver = new LiftedHomographySolver();
            for (TagDetection d : sets.small) {
                solver.addCorrespondence(d.cxy, SmallMosaic.getPosition(d.id));
            }

            Hsmall = solver.solve();
        }

        double[][] Hlarge = null;
        if (true) {
            LiftedHomographySolver solver = new LiftedHomographySolver();
            for (TagDetection d : sets.large) {
                solver.addCorrespondence(d.cxy, LargeMosaic.getPosition(d.id));
            }

            Hlarge = solver.solve();
        }

        JFrame jf = new JFrame();
        jf.setLayout(new BorderLayout());

        VisWorld vw = new VisWorld();
        VisLayer vl = new VisLayer(vw);
        VisCanvas vc = new VisCanvas(vl);

        vc.setBackground(Color.black);
        jf.add(vc, BorderLayout.CENTER);

        VisWorld.Buffer vb = vw.getBuffer("foo");

        ArrayList<double[]> vertices = new ArrayList<double[]>();
        ArrayList<double[]> vxLarge = new ArrayList<double[]>();
        ArrayList<double[]> vxSmall = new ArrayList<double[]>();
        for (TagDetection td : sets.small) {
            double i = td.cxy[0], j = td.cxy[1];
            double[] phi = new double[] {i*i, i*j, j*j, i, j , 1};

                double[] pLarge = LinAlg.matrixAB(Hlarge, phi);
                pLarge = LinAlg.scale(pLarge, 1.0/pLarge[2]);

                double[] pSmall = LinAlg.matrixAB(Hsmall, phi);
                pSmall = LinAlg.scale(pSmall, 1.0/pSmall[2]);

                LinAlg.printTranspose(pSmall);
                LinAlg.printTranspose(pLarge);
                System.out.println();

                pSmall[2] += 1.5 * 0.0254;
                vertices.add(pSmall);
                vertices.add(pLarge);

                vxLarge.add(pLarge);
                vxSmall.add(pSmall);

                if (td.id == 91) {
                    CameraPosition campos = vl.cameraManager.getCameraTarget();
                    vl.cameraManager.uiLookAt(new double[] {0.2, 0.1, 1.5}, pSmall, campos.up, true);
                }
            }

        vb.addBack(new VzLines(new VisVertexData(vertices), VzLines.LINES, new VzLines.Style(Color.white, 1)));
        vb.addBack(new VzPoints(new VisVertexData(vxLarge), new VzPoints.Style(Color.cyan, 5)));
        vb.addBack(new VzPoints(new VisVertexData(vxSmall), new VzPoints.Style(Color.red, 3)));

        vb.swap();

        jf.setSize(800, 800);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jf.setVisible(true);
    }
}

class LiftedHomographySolver
{
    ArrayList<double[]> constraint = new ArrayList<double[]>();

    public void addCorrespondence(double[] image, double[] world)
    {
        double i = image[0], j = image[1];
        double x = world[0], y = world[1];

        double i2 = i*i, j2 = j*j, ij = i*j;

        constraint.add(new double[]
                {-i2, -ij, -j2, -i, -j, -1, 0, 0, 0, 0, 0, 0, x*i2, x*ij, x*j2, x*i, x*j, x});
        constraint.add(new double[]
                {0, 0, 0, 0, 0, 0, -i2, -ij, -j2, -i, -j, -1, y*i2, y*ij, y*j2, y*i, y*j, y});
    }

    double[][] solve()
    {
        Matrix A = new Matrix(constraint.size(), constraint.get(0).length);
        for (int i=0; i<constraint.size(); ++i) {
            A.setRow(i, new DenseVec(constraint.get(i)));
        }

        SingularValueDecomposition svd = new SingularValueDecomposition(A);
        Matrix V = svd.getV();

        double[] h = V.getColumn(V.getColumnDimension()-1).copyArray();
        return new double[][] {
                { h[0],  h[1],  h[2],  h[3],  h[4],  h[5]},
                { h[6],  h[7],  h[8],  h[9], h[10], h[11]},
                {h[12], h[13], h[14], h[15], h[16], h[17]},
        };
    }
}
