import sys
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

pvalues = sys.argv[1]
stats = importr('stats')

with open(pvalues, 'r') as f:
    pval_hpv = []
    pval_smk = []
    pval_hpvsmk = []
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pval_hpv.append(float(line[6]))
        pval_smk.append(float(line[12]))
        pval_hpvsmk.append(float(line[18]))
    p_adjust_1 = stats.p_adjust(FloatVector(pval_hpv), method = 'BH')
    p_adjust_2 = stats.p_adjust(FloatVector(pval_smk), method = 'BH')
    p_adjust_3 = stats.p_adjust(FloatVector(pval_hpvsmk), method = 'BH')
    f.seek(0)
    hdr = f.readline()
    print '\t'.join([hdr.rstrip(), 'FDR_hpv', 'FDR_smoking', 'FDR_hpvsmoking'])
    i = 0
    for line in f:
        print '\t'.join([line.rstrip(), str(p_adjust_1[i]), str(p_adjust_2[i]), str(p_adjust_3[i])])
        i += 1