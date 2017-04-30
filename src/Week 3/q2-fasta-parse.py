from Bio import SeqIO
import gzip, re, sys

'''
This script opens a zipped fasta file and parses each record in
the fasta file, printing the accession and full sequence of each
as tab-separated output
'''

# open zipped fasta file provided as cmd line argument
with gzip.open(sys.argv[1], 'r') as f:
	# print header lines for output
	print '\t'.join(['Accession', 'Protein sequence'])
	# parse each fasta entry using SeqIO
	for record in SeqIO.parse(f, 'fasta'):
		# retrieve accession/ID for entry
		accession = '-'	
		if record.id: # if ID for entry exists
			accession = record.id
		# retrieve sequence for entry	
		sequence = '-'
		if record.seq: # if sequence for entry exists
			sequence = str(record.seq)
		# print accession and sequence as tab-sep fields on one line
		print '\t'.join([accession, sequence])	
