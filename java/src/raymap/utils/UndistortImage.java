package raymap.utils;

import java.awt.*;
import java.awt.image.*;

import javax.swing.*;

import april.vis.*;


public class UndistortImage
{
    static JFrame jf = new JFrame("Undistorted");
    static VisWorld vw = new VisWorld();
    static VisLayer vl = new VisLayer(vw);
    static VisCanvas vc = new VisCanvas(vl);

    static {
        jf.setLayout(new BorderLayout());
        jf.add(vc, BorderLayout.CENTER);
        jf.setSize(800, 800);
        jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    static int getRGB(BufferedImage im, double x, double y)
    {
        Color c = new Color(im.getRGB((int)x, (int)y));
        return ColorUtil.setAlpha(c, 128).getRGB();
    }

    /**
     * @param im
     * @param mappedxy[i][j] = {ux, uy}, the undistored(i,j)
     */
    public static void show(BufferedImage im, double[][][] mappedxy)
    {
        VisWorld.Buffer vb = vw.getBuffer("undistored");
        int W = im.getWidth();
        int H = im.getHeight();

        VisVertexData vvd = new VisVertexData();
        VisColorData vcd = new VisColorData();
        for (int i=0; i<W-1; ++i)
            for (int j=0; j<H-1; ++j) {
                /* Add quad */
                for (int[] xy : new int[][] {{i, j}, {i+1, j}, {i+1, j+1}, {i, j+1}}) {
                    double[] u = mappedxy[xy[0]][xy[1]];
                    vvd.add(new double[] {u[0], u[1], 0});
                    vcd.add(getRGB(im, xy[0], xy[1]));
                }
            }

        vb.addFront(new VzMesh(vvd, VzMesh.QUADS, new VzMesh.Style(vcd)));
        jf.setVisible(true);
    }
}