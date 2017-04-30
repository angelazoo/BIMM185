import sys

'''
Given fasta file input, script calculates the GC content
of all sequences in the file
'''

# path to fasta file given by cmd line argument
fasta = sys.argv[1]

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

gc_count = genome.count('G') + genome.count('C')
print "GC content:"
print float(gc_count)/len(genome)
