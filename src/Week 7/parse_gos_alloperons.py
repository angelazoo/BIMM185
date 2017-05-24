import sys

operons_all = {}
# open flat file containing gene name, pos, operon membership information
with open(sys.argv[1], 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        # extract operon, strand, position info
        operon = line[7]
        strand = line[4]
        left = int(line[5])
        right = int(line[6])
        if operon not in operons_all:
            operons_all[operon] = {}
            operons_all[operon][strand] = []
        # append left, right coordinates of gene to operon
        operons_all[operon][strand].append((left, right))
    # for each operon
    for operon in sorted(operons_all):
        for s in operons_all[operon]:
            # sort all coordinates by start pos
            tmp_g = sorted(operons_all[operon][s])
            # for each stop pos/start pos junction, calculate intergenic distance
            for g in xrange(0, len(tmp_g)-1):
                dist = tmp_g[g+1][0] - tmp_g[g][1]
                # print in tab sep table
                print operon, '\t', str(dist)   
