import sys, MySQLdb

hpv_pos = {} 
hpv_neg = {} 
yes_smk = {}
non_smk = {}
hpv_pos_non_smk = {}
hpv_neg_yes_smk = {}

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd=xxxxxxxx, db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
# hpv(+) patients
c.execute("""select pat_id from hnscc_clinical where hpv="Positive";""")
pts = c.fetchall()
for pt in pts:
	hpv_pos[pt[0]] = 1
# hpv(-) patients
c.execute("""select pat_id from hnscc_clinical where hpv="Negative";""")
pts = c.fetchall()
for pt in pts:
	hpv_neg[pt[0]] = 1
# smoker patients
c.execute("""select pat_id from hnscc_clinical where smoking_history="2" or smoking_history="4";""")
pts = c.fetchall()
for pt in pts:
	yes_smk[pt[0]] = 1
# nonsmoker patients
c.execute("""select pat_id from hnscc_clinical where smoking_history="1" or smoking_history="3";""")
pts = c.fetchall()
for pt in pts:
	non_smk[pt[0]] = 1
# hpv(+) nonsmoker
c.execute("""select pat_id from hnscc_clinical where hpv="Positive and (smoking_history="1" or smoking_history="3")";""")
pts = c.fetchall()
for pt in pts:
	hpv_pos_non_smk[pt[0]] = 1
# hpv(-) smoker 
c.execute("""select pat_id from hnscc_clinical where hpv="Negative" and (smoking_history="2" or smoking_history="4");""")
pts = c.fetchall()
for pt in pts:
	hpv_neg_yes_smk[pt[0]] = 1

# file containing list of filenames for patient MAF files
pt_filelist = sys.argv[1]
# dict to store mutation tallies as [gene[mutated_pt[1]]] structure
mut_tallies = {}
# list of shortened patient ids
pt_list = []
with open(pt_filelist, 'r') as f:
    for line in f:
	# strip filename suffix to obtain shortened pt id
        line = line.rstrip()
        pt = line.split('.')[0][:-3]
        pt_list.append(pt)
	# open listed filename
        with open(line, 'r') as f2:
	    # skip header
            f2.readline()
            for line in f2:
                line = line.rstrip().split('\t')
                mut = line[0]
                mut_type = line[8]
		# if nonsilent mutation, record pt as mutated pt in the mut_tallies dict
                if mut_type != "Silent":
                    if mut not in mut_tallies:
                        mut_tallies[mut] = {}
                    mut_tallies[mut][pt] = 1
        f2.close()
    f.close()  

# print output file header
print '\t'.join(["gene", "hpv+ "+str(len(hpv_pos)), "hpv- "+str(len(hpv_neg)), "smoker "+str(len(yes_smk)), "nonsmoker "+str(len(non_smk)), "hpv+nonsmoker "+str(len(hpv_pos_non_smk)), "hpv-smoker "+str(len(hpv_neg_yes_smk))])
for mut in mut_tallies:
	# if mutation occurs in 3% or more of the 510 hnscc pts
	if sum(mut_tallies[mut].values()) > 15:
		hpv_pos_count = 0
		hpv_neg_count = 0
		yes_smk_count = 0
		non_smk_count = 0
		hpv_pos_non_smk_count = 0
		hpv_neg_yes_smk_count = 0
		# determine number of mutations among pts in each cohort by iterating through all listed pats for the mutation in the
		# mut_tallies dict
		for pt in mut_tallies[mut]:
			if pt in hpv_pos:
				hpv_pos_count += 1
			elif pt in hpv_neg:
				hpv_neg_count += 1
			if pt in yes_smk:
				yes_smk_count += 1
			elif pt in non_smk:
				non_smk_count += 1
			if pt in hpv_pos_non_smk:
				hpv_pos_non_smk_count += 1
			elif pt in hpv_neg_yes_smk:
				hpv_neg_yes_smk_count += 1
		# print as tab-sep output the mutation counts for each cohort
		print '\t'.join([mut, str(hpv_pos_count), str(hpv_neg_count), str(yes_smk_count), str(non_smk_count), str(hpv_pos_non_smk_count), str(hpv_neg_yes_smk_count)])
  

	

