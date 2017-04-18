import matplotlib.pyplot as plt
import sys

# file name from command line
data = sys.argv[1]
proteins = sys.argv[2]

with open(data, 'r') as f, open(proteins, 'r') as f1:
    # x stores data of locus #, y stores CUI
    x = []
    y = []
    # separate data group for ribosomal proteins
    x_protein = []
    y_protein = []
    # list of colors of each point - red = ribosomal, blue = other
    color = []
    protein_list = {}
    # parse ribosomal protein list and save names of all ribo proteins
    for line in f1:
        line = line.rstrip().split('\t')
        protein_list[line[0]] = 1
    # parse protein-CUI list
    for line in f:
        line = line.rstrip().split('\t')
        # if protein is ribosomal, modify color list and add protein
        # score and name to ribo-specific data lists
        if line[0].rstrip() in protein_list:
            x_protein.append(int(line[0][1:].rstrip()))
            y_protein.append(float(line[1]))
            color.append('red')
        # if not ribosomal, then simply color protein coordinate blue
        else:
            color.append('blue')
        x.append(int(line[0][1:].rstrip()))
        y.append(float(line[1]))
    # CUI vs. chr order plot, separate series for ribo and other proteins
    plt.figure(1)
    plt.scatter(x, y, marker='.', c='blue', edgecolors='none')
    plt.scatter(x_protein, y_protein, marker='.', c='red', edgecolors='none')
    plt.title('CUI vs. genes in chromosomal order')
    plt.xlabel('Genes (chromosomal order)')
    plt.ylabel('Codon Usage Index')
    
    # CUI in ascending order plot 
    plt.figure(2)
    plt.scatter(range(1, len(y)+1), sorted(y), marker='.', c=color, edgecolors='none')
    plt.title('CUI vs. genes in ascending order')
    plt.xlabel('Genes (ascending order)')
    plt.ylabel('Codon Usage Index')
    plt.show()