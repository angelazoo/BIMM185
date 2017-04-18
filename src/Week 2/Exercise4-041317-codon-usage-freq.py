import sys, re

# generate list of codons from combination of bases
bases = ['A', 'C', 'G', 'T']
codons = [x+y+z for x in bases for y in bases for z in bases]
# partition codon list with start and stop codons sorted separately
# from others
starts = ['ATG']
stops = ['TAA', 'TAG', 'TGA']
others = [i for i in codons if i not in starts and i not in stops]

# read in file from command line
in_file = sys.argv[1]

with open(in_file, 'r') as f:
    # initialize global counter for each codon 
	global_counter = {c:0 for c in codons}
	base_count = 0
    # print header with gene names followed by codon counts (start codon + 
    # alpha sort, stop codons)
	print 'gene\t', starts[0], '\t', '\t'.join(c for c in sorted(others)), \
		'\t', '\t'.join(c for c in sorted(stops)), '\tlength'
    # for each line/seq in file
	for line in f:
        # initialize local (gene-level) counter for each codon
		local_counter = {c:0 for c in codons}
		line = line.rstrip().split("\t")
		protein = line[0]
		seq = line[1]
		# if protein length not multiple of 3, skip
		if len(seq) % 3 != 0:
			continue	
        # increment total base count by lengh of sequence
		base_count += len(seq)
        # generate list of 3-mers/codons in sequence
		gene_codons = re.findall('[ACGT]{3}', seq)
        # increment both local and global codon counts by identity
		for c in gene_codons:
			global_counter[c] += 1
			local_counter[c] += 1
        # print header and codon counts
		print protein, '\t', str(local_counter['ATG']), '\t', \
			'\t'.join(str(local_counter[c]) for c in sorted(others)),\
			'\t', '\t'.join(str(local_counter[c]) for c in sorted(stops)),\
			'\t', len(seq)/3
    # print bottom row (output global count of codons)
	print 'Totals\t', str(global_counter['ATG']), '\t', \
		'\t'.join(str(global_counter[c]) for c in sorted(others)),\
		'\t', '\t'.join(str(global_counter[c]) for c in sorted(stops)),\
		'\t', base_count/3 