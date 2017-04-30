import sys, os, gzip
from Bio import SwissProt

'''
This script downloads Archaea taxonomic information from Uniprot and then
parses the downloaded file to print the taxonomy ID, organism name and taxonomic
classification of each record in the file as tab-separated output
'''

# execute shell cmd to download taxonomic information file on all Archaea from Uniprot
os.system('wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_archaea.dat.gz')

# maintain a dictionary to keep track of existing tax_id's encountered
record_list = {}
# open zipped uniprot file and parse each record
for record in SwissProt.parse(gzip.open('uniprot_sprot_archaea.dat.gz')):
	# if record is not duplicate	
	if ''.join(record.taxonomy_id) not in record_list:
		# add to existing dictionary of encountered records (Tax_ids)
		record_list[''.join(record.taxonomy_id)] = 1	
		# print tax_id, organism name, and taxonomic classification as tab separated line
		print ''.join(record.taxonomy_id), '\t', str(record.organism), '\t', ', '.join(record.organism_classification)	
	
