import matplotlib.pyplot as plt
import sys

# file name from command line
data = sys.argv[1]

with open(data, 'r') as f:
    # x stores data of locus #, y stores CUI
    x = []
    y = []
     # parse protein-CUI list
    for line in f:
        # add protein score and name to data lists
        line = line.rstrip().split('\t')
        line[0] = line[0].rstrip()
        x.append(int(line[0][1:]))
        y.append(float(line[1]))
        xy = dict(zip(x,y))
    # CUI vs. chr order plot, separate series for ribo and other proteins
    plt.figure(1)
    plt.scatter([x for x in sorted(xy)], [xy[x] for x in sorted(xy)], marker='.',\
                 edgecolors='none')
    plt.title('CUI vs. genes in chromosomal order')
    plt.xlabel('Genes (chromosomal order)')
    plt.ylabel('Codon Usage Index')
    # CUI in ascending order plot  
    plt.figure(2)
    plt.scatter(range(1, len(y)+1), sorted(y), marker='.', edgecolors='none')
    plt.title('CUI vs. genes in ascending order')
    plt.xlabel('Genes (ascending order)')
    plt.ylabel('Codon Usage Index')
    # CUI histogram plot
    plt.figure(3)
    plt.hist(y)
    plt.title('Histogram of CUIs')
    plt.xlabel('Codon Usage Index')
    plt.ylabel('Count')
    plt.show()
