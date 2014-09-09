import fileinput
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys


if __name__ == '__main__':
#----------------------------------------
    font = {'size': 11}
    matplotlib.rc('font', **font)
    
    
    def parse(line_offset, subplot_a, subplot_b):
        a_mean = []
        a_max = []
        b_mean = []
        b_max = []
        
        stream = fileinput.input(sys.argv[1])
        for line in stream:
            if line.startswith(' Cross-validation results (validation)'):
                for _ in range(line_offset): stream.readline()
                
                a = stream.readline()
                b = stream.readline()
                
                a = a.split(': ')[1].strip()
                b = b.split(': ')[1].strip()
                a = a.replace('   ', ',').replace(' ', ',')
                b = b.replace('   ', ',').replace(' ', ',')
                
                a, b = list(eval(a)), list(eval(b))
                
                a_mean.extend(np.array(a)[range(0,len(a),2)])
                a_max.extend(np.array(a)[range(1,len(a),2)])
                b_mean.extend(np.array(b)[range(0,len(a),2)])
                b_max.extend(np.array(b)[range(1,len(a),2)])
                
        
        plt.subplot(*subplot_a)
        hist, bins = np.histogram(a_max, 16, (0,8))
        plt.bar(bins[0:-1], hist, width=0.3, color='#276419')
        hist, bins = np.histogram(b_max, 16, (0,8))
        plt.bar(bins[0:-1]+0.1, hist, width=0.3, color='#7fbc41', alpha=0.9)
        plt.yticks([0, 100, 200])
        plt.xlim((0,8))
        plt.gca().yaxis.tick_right()

        plt.subplot(*subplot_b)
        hist, bins = np.histogram(a_mean, 16, (0,6))
        plt.bar(bins[0:-1], hist, width=0.25, color='#276419', label='classic')
        hist, bins = np.histogram(b_mean, 16, (0,6))
        plt.bar(bins[0:-1]+0.08, hist, width=0.25, color='#7fbc41', alpha=0.9, label='augmented')
        plt.yticks([0, 175, 350])
        plt.xlim((0,6))
        plt.gca().yaxis.tick_right()
        

    parse(2, (3,2,1), (3,2,2))
    parse(6, (3,2,3), (3,2,4))
    parse(10, (3,2,5), (3,2,6))

    plt.subplot(3,2,1); plt.title('Max Test Err', fontsize=11)
    plt.subplot(3,2,2); plt.title('Mean Test Err', fontsize=11); plt.legend(prop={'size':11})
    
    plt.subplot(3,2,1); plt.ylabel('Tamron-2.2')
    plt.subplot(3,2,3); plt.ylabel('Tamron-2.8')
    plt.subplot(3,2,5); plt.ylabel('Tokina-3.3')

    plt.subplot(3,2,1); plt.gca().xaxis.set_ticklabels([])
    plt.subplot(3,2,2); plt.gca().xaxis.set_ticklabels([])
    plt.subplot(3,2,3); plt.gca().xaxis.set_ticklabels([])
    plt.subplot(3,2,4); plt.gca().xaxis.set_ticklabels([])

    plt.subplot(3,2,5); plt.xlabel('pixels')
    plt.subplot(3,2,6); plt.xlabel('pixels')
        
    plt.show()