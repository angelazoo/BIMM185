import sys, re

def revC(seq):
	'''
	Output reverse complement of input string
	'''
    # Dict mapping base to complement base
	comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    # Convert each base in input string to complement
	letters = [comp[s] for s in list(seq)]
    # Return reverse of result
	return ''.join(letters[::-1])

# interpret commandline args
fasta = sys.argv[1]
table = sys.argv[2]

# empty string to store genome
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
	# save start, stop, strand, tag fields in each line
	for line in f2:
		line = line.rstrip().split('\t')
		start = int(line[2])
		stop = int(line[3])
		strand = line[4]
		tag = line[7]
		# access sequence in genome based on start/stop pos
		seq = genome[start-1:stop]
		# if seq on reverse strand, output reverse complement  
		if strand == "-":
			seq = revC(seq)
		# print gene locus tag and sequence on one line sep by 
		# tab
		print tag, "\t", seq
