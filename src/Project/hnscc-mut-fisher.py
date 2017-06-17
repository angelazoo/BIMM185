import sys, scipy.stats

counts = sys.argv[1]

cohort_sizes = [] 
with open(counts, 'r') as f:
    print '\t'.join(['gene', 'mut_hpv+', 'wt_hpv+', 'mut_hpv-', 'wt_hpv-', 'odds_ratio', 'pvalue', 'mut_smoker', 'wt_smoker', 'mut_nonsmoker', 'wt_nonsmoker', 'odds_ratio', 'pvalue', 'mut_hpv+nonsmoker', 'wt_hpv+nonsmoker', 'mut_hpv-smoker', 'wt_hpv-smoker', 'odds_ratio', 'pvalue'])
    hdr = f.readline().strip().split('\t')
    # capture pat cohort sizes  
    for i in xrange(1, len(hdr)):
        cohort = hdr[i].split()
        cohort_sizes.append(int(cohort[1]))
    for line in f:
        line = line.rstrip().split('\t')
        gene = line[0]
        hpv_pos_mut = int(line[1])
        hpv_pos_wt = cohort_sizes[0] - hpv_pos_mut 
        hpv_neg_mut = int(line[2])
        hpv_neg_wt = cohort_sizes[1] - hpv_neg_mut
        oddsratio_1, pvalue_1 = scipy.stats.fisher_exact([[hpv_pos_mut, hpv_neg_mut], [hpv_pos_wt, hpv_neg_wt]])
        smoker_mut = int(line[3])
        smoker_wt = cohort_sizes[2] - smoker_mut
        nonsmoker_mut = int(line[4])
        nonsmoker_wt = cohort_sizes[3] - nonsmoker_mut
        oddsratio_2, pvalue_2 = scipy.stats.fisher_exact([[smoker_mut, nonsmoker_mut], [smoker_wt, nonsmoker_wt]])
        hpv_pos_nonsmoker_mut = int(line[5])
        hpv_pos_nonsmoker_wt = cohort_sizes[4] - hpv_pos_nonsmoker_mut
        hpv_neg_smoker_mut = int(line[6])
        hpv_neg_smoker_wt = cohort_sizes[5] - hpv_neg_smoker_mut
        oddsratio_3, pvalue_3 = scipy.stats.fisher_exact([[hpv_pos_nonsmoker_mut, hpv_neg_smoker_mut], [hpv_pos_nonsmoker_wt, hpv_neg_smoker_wt]])
        print '\t'.join([gene, str(hpv_pos_mut), str(hpv_pos_wt), str(hpv_neg_mut), str(hpv_neg_wt), str(oddsratio_1), str(pvalue_1), str(smoker_mut), str(smoker_wt), str(nonsmoker_mut), str(nonsmoker_wt), str(oddsratio_2), str(pvalue_2), str(hpv_pos_nonsmoker_mut), str(hpv_pos_nonsmoker_wt), str(hpv_neg_smoker_mut), str(hpv_neg_smoker_wt), str(oddsratio_3), str(pvalue_3)])