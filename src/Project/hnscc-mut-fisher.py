import sys, scipy.stats

# composite flat file containing number of mutations of each gene per cohort
counts = sys.argv[1]

cohort_sizes = [] 
with open(counts, 'r') as f:
    # print header line
    print '\t'.join(['gene', 'mut_hpv+', 'wt_hpv+', 'mut_hpv-', 'wt_hpv-', 'odds_ratio', 'pvalue', 'mut_smoker', 'wt_smoker', 'mut_nonsmoker', 'wt_nonsmoker', 'odds_ratio', 'pvalue', 'mut_hpv+nonsmoker', 'wt_hpv+nonsmoker', 'mut_hpv-smoker', 'wt_hpv-smoker', 'odds_ratio', 'pvalue'])
    hdr = f.readline().strip().split('\t')
    # capture pat cohort sizes from flat file header 
    for i in xrange(1, len(hdr)):
        cohort = hdr[i].split()
        cohort_sizes.append(int(cohort[1]))
    for line in f:
        line = line.rstrip().split('\t')
        # capture gene name
        gene = line[0]
        # record # hpv+ mutations and compute number of wt
        hpv_pos_mut = int(line[1])
        hpv_pos_wt = cohort_sizes[0] - hpv_pos_mut 
        # record # hpv- mutations and compute number of wt
        hpv_neg_mut = int(line[2])
        hpv_neg_wt = cohort_sizes[1] - hpv_neg_mut
        # fisher exact test of independence on mutational frequencies between hpv+ and hpv- cohorts
        oddsratio_1, pvalue_1 = scipy.stats.fisher_exact([[hpv_pos_mut, hpv_neg_mut], [hpv_pos_wt, hpv_neg_wt]])
        # record # smoker mutations and compute # of wt
        smoker_mut = int(line[3])
        smoker_wt = cohort_sizes[2] - smoker_mut
        # record # nuonsmoker mutaitons and compute # of wt
        nonsmoker_mut = int(line[4])
        nonsmoker_wt = cohort_sizes[3] - nonsmoker_mut
        # fisher exact test of independence on mutational frequencies between smoker and nonsmoker cohorts
        oddsratio_2, pvalue_2 = scipy.stats.fisher_exact([[smoker_mut, nonsmoker_mut], [smoker_wt, nonsmoker_wt]])
        # record number of hpv+ nonsmoker mutations and computer # of wt
        hpv_pos_nonsmoker_mut = int(line[5])
        hpv_pos_nonsmoker_wt = cohort_sizes[4] - hpv_pos_nonsmoker_mut
        # record number of hpv- smoker mutations and compute # of wt
        hpv_neg_smoker_mut = int(line[6])
        hpv_neg_smoker_wt = cohort_sizes[5] - hpv_neg_smoker_mut
        # fisher exact test of independence on mutational frequencies between hpv+ nonsmoker and hpv- smoker cohorts
        oddsratio_3, pvalue_3 = scipy.stats.fisher_exact([[hpv_pos_nonsmoker_mut, hpv_neg_smoker_mut], [hpv_pos_nonsmoker_wt, hpv_neg_smoker_wt]])
        # print tab-separated output of each cohort pair analysis (contingency tables and oddsratio/pvalue)
        print '\t'.join([gene, str(hpv_pos_mut), str(hpv_pos_wt), str(hpv_neg_mut), str(hpv_neg_wt), str(oddsratio_1), str(pvalue_1), str(smoker_mut), str(smoker_wt), str(nonsmoker_mut), str(nonsmoker_wt), str(oddsratio_2), str(pvalue_2), str(hpv_pos_nonsmoker_mut), str(hpv_pos_nonsmoker_wt), str(hpv_neg_smoker_mut), str(hpv_neg_smoker_wt), str(oddsratio_3), str(pvalue_3)])
