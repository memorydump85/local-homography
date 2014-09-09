package raymap.graph;


public interface IDistortionNode
{
    public abstract double[] apply(double[] p, double cx, double cy);
}
