import sys, numpy as np
import matplotlib.pylab as plt

# input file is flat file (tab-sep) consisting of gid1, gid2, distance, status, and
# calculated probability 
with open(sys.argv[1], 'r') as f:
    # initialize arrays for use in graphs
    # true pos and neg 
    tp = []
    tn = []
    # sensitiviy and specificity
    sens_arr = []
    spec_arr = []
    # precision
    prec_arr = []
    # true pos rate and false pos rate
    tpr_arr = []
    fpr_arr = []
    # accuracy 
    acc_arr = []

    # print header line for output table
    print '\t'.join(['cutoff', 'sensitivity', 'specificity', 'precision', 'tpr', 'fpr', 'accuracy']) 

    # parsing each line in input file
    for line in f:
        line = line.rstrip().split('\t')
        # if status is true positive, append prob to true pos array
        if line[3] == 'TP':
            tp.append(float(line[4]))
        # if status is true negative, append prob to true neg array
        elif line[3] == 'TN':
            tn.append(float(line[4]))
    
    # sort true pos and true neg arrays
    tp = sorted(tp)
    tn = sorted(tn, reverse = True)

    # array of cutoff probability values in increments of 0.05 from 0.00 to 1.00
    cutoffs = np.linspace(0.0, 1.00, 21)
    # for each cutoff value
    for c in cutoffs:
        # detected number of true positives: find idx of first value in array which
        # equals or exceeds the cutoff and subtract from total # of true positives
        detected_tp = len(tp) - next((i for i,v in enumerate(tp) if v >= c), len(tp))
        # undetected true pos (false negatives) is total # true pos - detected # true pos
        detected_fn = len(tp) - detected_tp
     
        # sensitivity = (detected # true pos)/(total # of true pos) 
        sens = float(detected_tp)/len(tp)
        # append to sensivity array
        sens_arr.append(sens)
      
        # detected number of true negs: find idx of first value in array which is less
        # than the cutoff, substract from total # of true negs
        detected_tn = len(tn) - next((i for i,v in enumerate(tn) if v < c), len(tn))
        # undetected true negs (false positives) = total true negs - detected # true negs
        detected_fp = len(tn) - detected_tn
      
        # specificity = (detected # of true negs)/(total # of true negs) 
        spec = float(detected_tn)/len(tn)
        # append to specificity array
        spec_arr.append(spec)
      
        # precision = detected # true pos/(total detected positives, true and false) 
        try:
            prec = detected_tp/float(detected_tp+detected_fp)
        # handle div/0 or 0/0 case
        except ZeroDivisionError:
            prec = "undefined" 
        # append to prec array
        prec_arr.append(prec)
    
        # true pos rate = # detected true pos/(# detected true pos + # det false negs) 
        tpr = float(detected_tp)/(detected_tp + detected_fn)
        # false pos rate = # detected false pos/(# detected true neg + # det false pos) 
        fpr = float(detected_fp)/(detected_tn + detected_fp)
        # append to tpr and fpr arrays
        tpr_arr.append(tpr)
        fpr_arr.append(fpr)

        # accuracy = (# correct detections, true pos & false neg)/(total number of vals)
        acc = float(detected_tp + detected_tn)/(detected_tp+detected_fn+detected_tn+detected_fp) 
        # append to accuracy array
        acc_arr.append(acc) 
        
        # print stats for each cutoff value
        print '\t'.join(str(x) for x in [c, sens, spec, prec, tpr, fpr, acc])
    
    # plot sensitivity and specificity vs. cutoff value    
    plt.figure(1)
    plt.plot(cutoffs, sens_arr, label="sensitivity", color="r")
    plt.plot(cutoffs, spec_arr, label="specificity", color="b")
    plt.title("Sensitivity and Specificity vs. Probability Cutoff")
    plt.xlabel('Posterior cutoff')
    plt.ylabel('Performance')
    plt.legend(loc=6)

    # plot TPR vs. FPR    
    plt.figure(2)
    plt.plot(fpr_arr, tpr_arr, label="ROC", color="black")
    plt.plot([0, 1], [0, 1], label="No discrimination line", color="gray", linestyle=':') 
    plt.title("TPR vs. FPR")
    plt.xlabel('False positive rate (1 - Specificity)')
    plt.ylabel('True positive rate')
    plt.legend(loc=4)

    # plot accuracy vs. cutoff value
    plt.figure(3)
    plt.plot(cutoffs, acc_arr, color="black")
    plt.title("Accuracy vs. Probability Cutoff")
    plt.xlabel('Posterior cutoff')     
    plt.ylabel('Accuracy')
    plt.show()
