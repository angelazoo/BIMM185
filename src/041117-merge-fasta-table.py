import sys, re

def revC(seq):
	'''
	Output reverse complement of input string
	'''
	comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
	letters = [comp[s] for s in list(seq)]
	return ''.join(letters[::-1])

fasta = sys.argv[1]
table = sys.argv[2]

genome = ''
# open fasta file
with open(fasta, 'r') as f1:
	# concatenate all non-header lines (seqs) into genome
	for line in f1:
		line = line.rstrip()
		if line[0] != '>':
			genome += line

# open protein table
with open(table, 'r') as f2:
	# skip header line
	f2.readline()
	# save start/stop, strand, locus, tag, protein names from
	# respective fields in each line
	for line in f2:
		line = line.rstrip().split('\t')
		start = int(line[2])
		stop = int(line[3])
		strand = line[4]
		locus = line[6]
		tag = line[7]
		protein = line[8]
		# print protein/locus/tag names
		print ">" + protein + "|" + locus + "|" + tag
		# get sequence from start/stop range in genome
		seq = genome[start-1:stop]  
		# if seq on reverse strand, then generate reverse
		# complementary sequence
		if strand == "-":
			seq = revC(seq)
		# print sequence in 70-nt increments on lines following
		# sequence header
		while len(seq) > 0:    
			print seq[:70] 
			seq = seq[70:]	
