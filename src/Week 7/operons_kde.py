from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pylab as plt
import sys

infile = sys.argv[1]
data1 = []

infile2 = sys.argv[2]
data2 = []

testdata = sys.argv[3]
data3 = []

with open(infile, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        data1.append(int(line[-1])) 
    f.close()

with open(infile2, 'r') as f2:
    for line in f2:
        line = line.rstrip().split('\t')
        data2.append(int(line[-1]))
    f2.close()

with open(testdata, 'r') as f3:
    for line in f3:
        line = line.rstrip().split('\t')
        data3.append(int(line[-1]))   
    f3.close()
 
kde1 = gaussian_kde(data1, bw_method=0.5)
kde2 = gaussian_kde(data2, bw_method=0.5)
data3 = sorted(data3)
a_pdf1 = kde1.evaluate(data3)
a_pdf2 = kde2.evaluate(data3)
max_2 = max(a_pdf2)
a_pdf1_norm = [i/max_2 for i in a_pdf1]
a_pdf2_norm = [i/max_2 for i in a_pdf2]
x = [i * 0.4 for i in a_pdf1] 
y = [i * 0.6 for i in a_pdf2]
z = [x+y for x,y in zip(x,y)]
x = [i * 0.4 for i in a_pdf1] 
y = [i * 0.6 for i in a_pdf2]
a_pdf3= [y/z for y,z in zip(y,z)]

plt.figure()
plt.plot(data3, a_pdf1_norm, label='p(d_i,j=x | h_0)', color="r")
plt.plot(data3, a_pdf2_norm, label='p(d_i,j=x | h_1)', color="g")
plt.plot(data3, a_pdf3, label='p(h_1 | d_i,j=x)', color="black")
plt.xlim([-10, 500])
plt.legend()
plt.show()