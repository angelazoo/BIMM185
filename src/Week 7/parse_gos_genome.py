import sys

with open(sys.argv[1], 'r') as f:
    curr_strand = ''
    curr_gene = ''
    for line in f:
        line = line.rstrip().split('\t')
        gene = line[1]
        strand = line[4]
        if strand != curr_strand and curr_strand != '':
            # do not calculate distances
            pass
        elif curr_strand != '':
            left = int(line[5])
            dist = left - curr_right
            print '\t'.join([curr_gene, gene, str(dist)])   
        curr_right = int(line[6])
        curr_strand = strand
        curr_gene = gene
        if curr_gene == 'b4403':
            break
    f.close() 
