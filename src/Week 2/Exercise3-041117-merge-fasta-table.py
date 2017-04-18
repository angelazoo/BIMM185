import sys, re

def revC(seq):
	'''
	Outputs reverse complement of input string
	'''
    # Dict mapping base to complement base
	comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    # Convert each base in input string to complement
	letters = [comp[s] for s in list(seq)]
    # Return reverse of result
	return ''.join(letters[::-1])

# read command line args
# first line is name of fasta file
fasta = sys.argv[1]
# second line is table of gene annotations
table = sys.argv[2]

# empty string to store genome
genome = ''
# open fasta file
with open(fasta, 'r') as f1:
	# concatenate all seqs into genome
	for line in f1:
		line = line.rstrip()
        # check that line is not header
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
        # save positional fields 
		start = int(line[2])
		stop = int(line[3])
        # save +/- strand information
		strand = line[4]
        # save locus/tag ID
		locus = line[6]
		tag = line[7]
        # save protein name
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
