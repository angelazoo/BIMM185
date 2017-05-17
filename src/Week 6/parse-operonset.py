import sys, re

# GeneProductSet.txt
genelist = sys.argv[1]
# OperonSet.txt
operon = sys.argv[2]

# define dictionaries to hold data
gene_ids = {}
operons = {}

# open GeneProductSet.txt
with open(genelist, 'r') as f1:
	# read each line
	for line in f1:
		# if line is not header line
		if re.search("^#", line) is None:
			# tab-separated info on each line
			line = line.rstrip().split('\t')
			# for each gene with a locus tag, create k,v pair for gene name and locus tag
			if len(line) >= 3:
				gene_ids[line[1]] = line[2]

with open(operon, 'r') as f:
	for line in f:
		if re.search("^#", line) is None:
			line = line.rstrip().split('\t')
			if len(line) >= 8:
					conf_level = line[7]
					if conf_level == 'Strong' or conf_level == 'Confirmed':
						if line[0] not in operons:
							operons[line[0]] = {}
							genes = line[5].split(',')
							for g in genes:
								operons[line[0]][g] = 1
								print line[0], '\t', g, '\t', gene_ids[g]
