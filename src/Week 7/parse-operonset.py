import sys, re

'''
This script parses the OperonSet and GeneProducts files to extract gene and operon information
for high confidence/confirmed operons
'''

# gene products file
genelist = sys.argv[1]
# operon set file
operon = sys.argv[2]
gene_ids = {}
operons = {}

with open(genelist, 'r') as f1:
    for line in f1:
        # skip header lines
        if re.search("^#", line) is None:
            line = line.rstrip().split('\t')
            # if locus_tag exists, create k,v pair for gene, locus tag
            if len(line) >= 3:
                gene_ids[line[1]] = line[2]

with open(operon, 'r') as f:
    for line in f:
        # skip header lines
        if re.search("^#", line) is None:
            line = line.rstrip().split('\t')
            # if operon has all fields
            if len(line) >= 8:
                    # if conf_level for being operon is strong or confirmed
                    conf_level = line[7]
                    if conf_level == 'Strong' or conf_level == 'Confirmed':
                        #  create k,v pair for operon, constituent genes
                        if line[0] not in operons:
                            operons[line[0]] = {}
                            genes = line[5].split(',')
                            for g in genes:
                                operons[line[0]][g] = 1
                                # for each gene, print operon name, gene, locus_tag
                                print line[0], '\t', g, '\t', gene_ids[g]
