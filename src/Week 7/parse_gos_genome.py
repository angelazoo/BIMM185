import sys

# read file containing gene, positional information, and exon membership for all
# genes in genome
with open(sys.argv[1], 'r') as f:
    curr_strand = ''
    curr_gene = ''
    for line in f:
        line = line.rstrip().split('\t')
        # extract gene name and strand information 
        gene = line[1]
        strand = line[4]
        # if gene pairs not on same strand
        if strand != curr_strand and curr_strand != '':
            # do not calculate distances
            pass
        # if current strand is not null (very start)
        elif curr_strand != '':
            # calculate intergenic distance
            left = int(line[5])
            dist = left - curr_right
            # print gene pair and intergenic distance as tab sep output 
            print '\t'.join([curr_gene, gene, str(dist)])   
        curr_right = int(line[6])
        curr_strand = strand
        curr_gene = gene
        # stop at the end of the e. coli genome
        if curr_gene == 'b4403':
            break
    f.close() 
