from scipy.stats import gaussian_kde
import numpy as np
import sys

# path to file with neg control distances
infile = sys.argv[1]
data1 = []

# path to file with pos control distances
infile2 = sys.argv[2]
data2 = []

# path to file with genome-wide distances
testdata = sys.argv[3]

# path to flat file with all operon membership info for each gene
table = sys.argv[4]

# open negative control distances
with open(infile, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        # append each distance to data1 array 
        data1.append(int(line[-1])) 
    f.close()

# calculate density function for data1
kde1 = gaussian_kde(data1, bw_method=0.5)

# opern pos control distances
with open(infile2, 'r') as f2:
    for line in f2:
        line = line.rstrip().split('\t')
        # append each distance to data2 array
        data2.append(int(line[-1]))
    f2.close()

# calculate density function for data2
kde2 = gaussian_kde(data2, bw_method=0.5)

gos = {}
# reading genes-operons flat file, make dict of k,v pairs for each gene and assoc
# operon 
with open(table, 'r') as f4:
    for line in f4:
        line = line.strip().split('\t')
        gene = line[1]
        operon = line[7]
        gos[gene] = operon     

# reading genomewide intergenic distances
with open(testdata, 'r') as f3:
    for line in f3:
        line = line.rstrip().split('\t')
        # name of geneids associated with intergenic distance
        g1 = line[0]
        g2 = line[1]
        # extract intergenic distance
        data3 = [int(line[-1])]
        # evaluate densities for the intergenic distance
        a_pdf1 = kde1.evaluate(data3)
        a_pdf2 = kde2.evaluate(data3)
        # calculate posterior probability
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        z = [x+y for x,y in zip(x,y)]
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        # posterior probability value
        a_pdf3 = [y/z for y,z in zip(y,z)][0]
        # handle NaN case
        if a_pdf3 != a_pdf3:
            a_pdf3 = 0
        # determine true positive, true negative, or undetermined status for genes
        status = ''  
        if gos[g1] != 'None' and gos[g2] != 'None' and gos[g1] == gos[g2]: 
            status = 'TP'
        elif gos[g1] != gos[g2]:
            status = 'TN'
        # print gene_id, distance, status, probability as tab-sep line
        print '\t'.join([g1, g2, str(data3[0]), status, str(a_pdf3)]) 
    f3.close()
 from scipy.stats import gaussian_kde
import numpy as np
import sys

# path to file with neg control distances
infile = sys.argv[1]
data1 = []

# path to file with pos control distances
infile2 = sys.argv[2]
data2 = []

# path to file with genome-wide distances
testdata = sys.argv[3]

# path to flat file with all operon membership info for each gene
table = sys.argv[4]

# open negative control distances
with open(infile, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        # append each distance to data1 array 
        data1.append(int(line[-1])) 
    f.close()

# calculate density function for data1
kde1 = gaussian_kde(data1, bw_method=0.5)

# opern pos control distances
with open(infile2, 'r') as f2:
    for line in f2:
        line = line.rstrip().split('\t')
        # append each distance to data2 array
        data2.append(int(line[-1]))
    f2.close()

# calculate density function for data2
kde2 = gaussian_kde(data2, bw_method=0.5)

gos = {}
# reading genes-operons flat file, make dict of k,v pairs for each gene and assoc
# operon 
with open(table, 'r') as f4:
    for line in f4:
        line = line.strip().split('\t')
        gene = line[1]
        operon = line[7]
        gos[gene] = operon     

# reading genomewide intergenic distances
with open(testdata, 'r') as f3:
    for line in f3:
        line = line.rstrip().split('\t')
        # name of geneids associated with intergenic distance
        g1 = line[0]
        g2 = line[1]
        # extract intergenic distance
        data3 = [int(line[-1])]
        # evaluate densities for the intergenic distance
        a_pdf1 = kde1.evaluate(data3)
        a_pdf2 = kde2.evaluate(data3)
        # calculate posterior probability
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        z = [x+y for x,y in zip(x,y)]
        x = [i * 0.4 for i in a_pdf1] 
        y = [i * 0.6 for i in a_pdf2]
        # posterior probability value
        a_pdf3 = [y/z for y,z in zip(y,z)][0]
        # handle NaN case
        if a_pdf3 != a_pdf3:
            a_pdf3 = 0
        # determine true positive, true negative, or undetermined status for genes
        status = ''  
        if gos[g1] != 'None' and gos[g2] != 'None' and gos[g1] == gos[g2]: 
            status = 'TP'
        elif gos[g1] != gos[g2]:
            status = 'TN'
        # print gene_id, distance, status, probability as tab-sep line
        print '\t'.join([g1, g2, str(data3[0]), status, str(a_pdf3)]) 
    f3.close()
