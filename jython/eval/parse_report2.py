import fileinput
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys


if __name__ == '__main__':
#----------------------------------------
    font = {'size': 10}
    matplotlib.rc('font', **font)
    
    
    def parse(line_offset, subplot):
        a_mean = []
        b_mean = []
        
        stream = fileinput.input(sys.argv[1])
        for line in stream:
            if line.startswith(' Straightness results'):
                for _ in range(line_offset): stream.readline()
                
                a = stream.readline()
                b = stream.readline()
                
                a = a.split(': ')[1].strip()
                b = b.split(': ')[1].strip()
                a = a.replace('   ', ',').replace(' ', ',')
                b = b.replace('   ', ',').replace(' ', ',')
                
                a, b = list(eval(a)), list(eval(b))
                a_mean.extend(np.array(a)[range(0, len(a), 2)])
                b_mean.extend(np.array(b)[range(0, len(b), 2)])
        
        plt.subplot(*subplot)
        hist, bins = np.histogram(a_mean, 32, (0,3))
        plt.bar(bins[0:-1], hist, width=0.04, color='#c51b7d', label='classic')
        hist, bins = np.histogram(b_mean, 32, (0,3))
        plt.bar(bins[0:-1]+0.03, hist, width=0.04, color='#f1b6da', alpha=0.9, label='augmented')
        plt.yticks([0, 20, 40])
        plt.xlim((0,1))
        plt.gca().yaxis.tick_right()

    parse(2, (3,1,1))
    parse(6, (3,1,2))
    parse(10, (3,1,3))

    plt.subplot(3,1,1); plt.title('Max deviation from straightness', fontsize=10)
    plt.legend(prop={'size':10})
     
    plt.subplot(3,1,1); plt.ylabel('Tamron-2.2'); plt.gca().xaxis.set_ticklabels([])
    plt.subplot(3,1,2); plt.ylabel('Tamron-2.8'); plt.gca().xaxis.set_ticklabels([])
    plt.subplot(3,1,3); plt.ylabel('Tokina-3.3'); plt.xlabel('pixels')
        
    plt.show()