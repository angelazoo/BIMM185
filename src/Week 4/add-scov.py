import sys

with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.strip().split('\t')
		scov = float(line[8])/float(line[3])
		line.append(str(scov))
		print '\t'.join(line)	
