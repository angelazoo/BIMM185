from scipy.stats import gaussian_kde
import numpy as np
import sys

infile = sys.argv[1]
data1 = []

infile2 = sys.argv[2]
data2 = []

testdata = sys.argv[3]
#data3 = []

table = sys.argv[4]

with open(infile, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        data1.append(int(line[-1])) 
    f.close()
kde1 = gaussian_kde(data1, bw_method=0.5)

with open(infile2, 'r') as f2:
    for line in f2:
        line = line.rstrip().split('\t')
        data2.append(int(line[-1]))
    f2.close()
kde2 = gaussian_kde(data2, bw_method=0.5)

gos = {}
with open(table, 'r') as f4:
    for line in f4:
        line = line.strip().split('\t')
        gene = line[1]
        operon = line[7]
        gos[gene] = operon     

with open(testdata, 'r') as f3:
    for line in f3:
        line = line.rstrip().split('\t')
        g1 = line[0]
        g2 = line[1]
        data3 = [int(line[-1])]
        a_pdf1 = kde1.evaluate(data3)
        a_pdf2 = kde2.evaluate(data3)
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        z = [x+y for x,y in zip(x,y)]
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        a_pdf3 = [y/z for y,z in zip(y,z)][0]
        # handle NaN case
        if a_pdf3 != a_pdf3:
            a_pdf3 = 0
        status = ''  
        if gos[g1] != 'None' and gos[g2] != 'None' and gos[g1] == gos[g2]: 
            status = 'TP'
        elif gos[g1] != gos[g2]:
            status = 'TN'
        print '\t'.join([g1, g2, str(data3[0]), status, str(a_pdf3)]) 
    f3.close()
 