import sys, os, re

'''
This script downloads README file for Uniprot reference proteomes and parses it to download proteomes
(that match user-defined keyword) to individual folders
'''

# execute shell cmd to download README file from Uniprot reference proteomes site to current directory
os.system('wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README')

# open README
with open('README', 'r') as f:
	id_list = []
	for line in f:
		line = line.rstrip()
		# if line in README matches keyword provided by cmd line argument (e.g. proteome/tax ID, species name)
		# add proteome id to list of IDs to download 
		if re.search(sys.argv[1], line):
			line = line.split()
			id_list.append(line[0])
	# execute shell cmd to download reference proteome for each id in list of IDs and save to folder whose name is ID
	for i in id_list:
		os.system('wget -P {} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/{}_*'.format(i, i))
