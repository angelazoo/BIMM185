import sys

operons_all = {}
with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.rstrip().split('\t')
		operon = line[7]
		strand = line[4]
		left = int(line[5])
		right = int(line[6])
		if operon not in operons_all:
			operons_all[operon] = {}
			operons_all[operon][strand] = []
		operons_all[operon][strand].append((left, right))
	for operon in sorted(operons_all):
		for s in operons_all[operon]:
			tmp_g = sorted(operons_all[operon][s])
			for g in xrange(0, len(tmp_g)-1):
				dist = tmp_g[g+1][0] - tmp_g[g][1]
				print operon, '\t', str(dist)	
				
				
