import sys, re

'''
Parses headers in input and extracts and reformats gene identifiers,
followed by second column containing the gene sequence as a one-line
string
'''

fasta = sys.argv[1]

# read in input
with open(fasta, 'r') as f:
	curr = ()
	genes = {}
	for line in f:
		line = line.rstrip()
		# if header line	
		if line[0] == '>':
			# capture IDs of interest from header and save as tuple
			match = re.search("^>gnl\|TC-DB\|(.*?)\|([A-Za-z\d\.]*)", line)
			curr = (match.group(2), match.group(1))
			genes[curr] = ''
		else:
			# if sequence line, append to any previous sequence associated with gene
			if len(curr) != 0:
				genes[curr] += line

	# print formatted output for each gene
	for s in genes:
		print '-'.join(e for e in s) + "\t" + genes[s]	
