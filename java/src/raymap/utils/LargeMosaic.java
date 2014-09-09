package raymap.utils;

import java.util.*;

import april.tag.*;

public class LargeMosaic
{
    static TagFamily tf = new Tag36h11();
    static HashMap<Integer, TagPosition> tagPositions = new HashMap<Integer, TagPosition>();

    static {
        final int TAGS_PER_ROW = 24;
        for (int y = 0; y < 24; y++) {
            for (int x = 0; x < TAGS_PER_ROW; x++) {
                TagPosition tp = new TagPosition();
                tp.id = (176-(y*TAGS_PER_ROW)) + x;

                if (tp.id >= tf.codes.length)
                    continue;

                /* NOTE: assumes one and half inch spacing between tags. */
                tp.cx = x * 1.5* 0.0254;
                tp.cy = y * 1.5* 0.0254;

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