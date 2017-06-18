import sys
import MySQLdb
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

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd=xxxxxxxx, db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
c.execute("""create table if not exists cohort_results (gene varchar(20) not null, hpv_pos_mut int(10) not null, hpv_pos_wt int(10) not null, hpv_neg_mut int(10) not null, hpv_neg_wt int(10) not null, oddsratio_1 float not null, pvalue_1 float not null, smoker_mut int(10) not null, smoker_wt int(10) not null, nonsmoker_mut int(10) not null, nonsmoker_wt int(10) not null, oddsratio_2 float not null, pvalue_2 float not null, hpvpos_nonsmoker_mut int(10) not null, hpvpos_nonsmoker_wt int(10) not null, hpvpos_smoker_mut int(10) not null, hpvpos_smoker_wt int(10) not null, oddsratio_3 float not null, pvalue_3 float not null, bh_1 float not null, bh_2 float not null, bh_3 float not null);""") 
c.execute("""load data local infile '/home/linux/ieng6/bm185s/azou/Final-project/mut-fisher_BH_15.txt' into table cohort_results (gene, hpv_pos_mut, hpv_pos_wt, hpv_neg_mut, hpv_neg_wt, oddsratio_1, pvalue_1, smoker_mut, smoker_wt, nonsmoker_mut, nonsmoker_wt, oddsratio_2, pvalue_2, hpvpos_nonsmoker_mut, hpvpos_nonsmoker_wt, hpvpos_smoker_mut, hpvpos_smoker_wt, oddsratio_3, pvalue_3, bh_1, bh_2, bh_3);""")
