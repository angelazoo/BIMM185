import sys

# command-line arg (tab-sep file)
in_file = sys.argv[1]

# with open file
with open(in_file, 'r') as f:
    # read lines in file
	lines = f.readlines()
    # last lines in file correspond to total codon counts in whole genome
    # strip very last column (total number of codons)
	genome_totals = [float(x) for x in lines[-1].rstrip().split('\t')[1:]]
    # generate proportions for each codon count (codon count / total # of
    # all codons) 
	p = [x/genome_totals[-1] for x in genome_totals[:-1]]
    # header contains codon names	
    codon_names = lines[0].rstrip().split('\t')[1:-1]
    # make dictionary of global codon frequencies
	codon_p = dict(zip(codon_names, p))
    # for remaining lines in file
	for i in xrange(1, len(lines)-1):
		gene_totals = lines[i].rstrip().split('\t')
        # save gene name field
		gene = gene_totals[0]
        # calculate gene-level codon frequencies
		q = [float(x)/float(gene_totals[-1]) for x in gene_totals[1:-1]]
        # bundle into dictionary
		codon_q = dict(zip(codon_names, q))
        # codon usage index calculation using global and local/gene-level
        # dictionaries
		CUI = sum(codon_p[i] * codon_q[i] for i in codon_names)
        # format output: gene name + codon usage index
		print gene, "\t", str(CUI)		 	
