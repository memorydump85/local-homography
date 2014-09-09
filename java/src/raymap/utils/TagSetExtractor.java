package raymap.utils;

import java.awt.image.*;
import java.util.*;

import april.jmat.*;
import april.tag.*;
import april.util.*;


public class TagSetExtractor
{
    static TagFamily tf = new Tag36h11();
    static TagDetector td = new TagDetector(tf);

    public static TagSet getTagSets(BufferedImage im)
    {
        ArrayList<TagDetection> detections =
                td.process(im, new double[] {im.getWidth()/2.0, im.getHeight()/2.0});

        UnionFindSimple ufs = new UnionFindSimple(detections.size());
        for (int i=0; i<detections.size(); ++i) {
            for (int j=0; j<detections.size(); ++j) {
                TagDetection d1 = detections.get(i);
                TagDetection d2 = detections.get(j);

                if (LinAlg.distance(d1.cxy, d2.cxy) < 50) {
                    if (Math.abs(d1.id-d2.id) == 1
                            || Math.abs(d1.id-d2.id) == 24
                            || Math.abs(d1.id-d2.id) == 14) {
                        ufs.connectNodes(i, j);
                    }
                }
            }
        }

        TagSet sets = new TagSet();

        for (int i=0; i<detections.size(); ++i) {
            if (ufs.getRepresentative(0) == ufs.getRepresentative(i)) {
                sets.small.add(detections.get(i));
            } else {
                sets.large.add(detections.get(i));
            }
        }

        return sets;
    }

    public static class TagSet
    {
        public ArrayList<TagDetection> small = new ArrayList<TagDetection>();
        public ArrayList<TagDetection> large = new ArrayList<TagDetection>();
    }
}
