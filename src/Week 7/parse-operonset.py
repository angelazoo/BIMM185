import sys, re

genelist = sys.argv[1]
operon = sys.argv[2]
gene_ids = {}
operons = {}

with open(genelist, 'r') as f1:
	for line in f1:
		if re.search("^#", line) is None:
			line = line.rstrip().split('\t')
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
