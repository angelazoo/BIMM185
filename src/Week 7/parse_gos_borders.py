import sys

with open(sys.argv[1], 'r') as f:
	curr_operon = ''
	curr_strand = ''
	for line in f:
		line = line.rstrip().split('\t')
		strand = line[4]
		operon = line[7]
		if strand != curr_strand and curr_strand != '':
			# do not calculate distances
			pass
		elif operon != curr_operon and curr_operon != '':
			left = int(line[5])
			dist = left - curr_right
			print '\t'.join([curr_operon, operon, str(dist)]) 	
		curr_right = int(line[6])
		curr_strand = strand
		curr_operon = operon
