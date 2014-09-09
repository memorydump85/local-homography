import numpy as np
import matplotlib.pyplot as plt
import matplotlib


if __name__ == '__main__':
#----------------------------------------
    x = np.array(np.arange(0, 3, 0.01))
    t = x + np.sin(2*x) + 0.45*np.random.rand(len(x))
    
    #matplotlib.pyplot.xkcd()
    plt.axvspan(x[220], xmax=x[250], facecolor='0.3', alpha=0.2)
    plt.annotate('W', (x[230], 0), color='0.2')

    plt.scatter(x, t, s=25, c='k', marker='+', linewidths=1)
    
    plt.scatter(x[220:250], t[220:250], s=25, c='r', marker='o', linewidths=0)    
    regressor = np.polyfit(x[220:250], t[220:250], 1)
    ry = np.polyval(regressor, x[180:280])
    plt.plot(x[180:280], ry, 'r-')
    
    plt.scatter(x[100:130], t[100:130], s=25, c='r', marker='o', linewidths=0)    
    regressor = np.polyfit(x[100:130], t[100:130], 1)
    ry = np.polyval(regressor, x[60:160])
    plt.plot(x[60:160], ry, 'r-')
    
    y = []    
    for i in xrange(len(x)):
        nbr = range(max(i-20,0), min(i+20, len(x)-1))
        regressor = np.polyfit(x[nbr], t[nbr], 1)
        ry = np.polyval(regressor, x[i])
        y.append(ry)

    plt.plot(x, y, 'b-', linewidth=4, alpha=0.4)
    plt.xlim([-0.1, 3.1])
    plt.ylim([-0.1, 3.1])
    
    plt.show()
