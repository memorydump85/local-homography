package raymap.utils;

import java.util.*;

import april.tag.*;

public class SmallMosaic
{
    static TagFamily tf = new Tag36h11();
    static HashMap<Integer, TagPosition> tagPositions = new HashMap<Integer, TagPosition>();

    static {
        final int TAGS_PER_ROW = 24;
        for (int y = 0; y < 24; y++) {
            for (int x = 0; x < TAGS_PER_ROW; x++) {
                TagPosition tp = new TagPosition();
                tp.id = (23+(y*TAGS_PER_ROW)) - x;

                if (tp.id >= tf.codes.length)
                    continue;

                /* NOTE: assumes one inch spacing between tags. */
                tp.cx = (3.75 + x) * 0.0254 + 0.014;
                tp.cy = (0.75 + y) * 0.0254 + 0.007;

                tagPositions.put(tp.id, tp);
            }
        }
    }

    static public double[] getPosition(int id)
    {
        TagPosition tp = tagPositions.get(id);
        return new double[] {tp.cx, tp.cy};
    }
}
