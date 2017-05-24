import sys

'''
This script calculates all intergenic distances corresponding to the negative
control (adjacent genes not in the same operon
'''

# reading flat file containing gene, operon membership and positional data
with open(sys.argv[1], 'r') as f:
    curr_operon = ''
    curr_strand = ''
    for line in f:
        line = line.rstrip().split('\t')
        # extract strand and operon name 
        strand = line[4]
        operon = line[7]    
        # if strand between pairs of genes is not the same
        if strand != curr_strand and curr_strand != '':
            # do not calculate distances
            pass
        # if operon between pairs of genes is not the same and previous is not null
        elif operon != curr_operon and curr_operon != '':
            # calculate intergenic distance
            left = int(line[5])
            dist = left - curr_right
            # print gene1 operon name, gene2 operon name, and intergenic distance
            print '\t'.join([curr_operon, operon, str(dist)])   
        # update current stop position, strand, and operon information
        curr_right = int(line[6])
        curr_strand = strand
        curr_operon = operon
