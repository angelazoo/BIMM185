import sys, numpy as np

with open(sys.argv[1], 'r') as f:
    tp = []
    tn = []
    print '\t'.join(['cutoff', 'sensitivity', 'specificity']) 
    for line in f:
        line = line.rstrip().split('\t')
        if line[3] == 'TP':
            tp.append(float(line[4]))
        elif line[3] == 'TN':
            tn.append(float(line[4]))
    tp = sorted(tp)
    tn = sorted(tn, reverse = True)
    cutoffs = np.linspace(0.0, 1.00, 21)
    for c in cutoffs:
        detected_tp = len(tp) - next((i for i,v in enumerate(tp) if v >= c), len(tp))
        sens = float(detected_tp)/len(tp)
        detected_tn = len(tn) - next((i for i,v in enumerate(tn) if v < c), len(tn))
        spec = float(detected_tn)/len(tn)
        print '\t'.join(str(x) for x in [c, sens, spec])