from Bio import SeqIO
import gzip
import re
import sys

'''
Script opens zipped genbank files and parses each record for information
about genome corresponding to the record. Prints as tab-separated output
the following files:
genomes.txt
replicons.txt
genes.txt
extrefs.txt
exons.txt
synonyms.txt
functiions.txt
which can be established as relational databases in SQL'''

# open file specified by cmd line argument containing filepaths to genbank
# files of interest
with open(sys.argv[1], 'r') as f:
	# initialize total number of genomes across all files
	genome_id = 0
	# initialize total number of replicons across all files 
	replicon_id = 0
	# initialize total number of cds across all files
	gene_id = 0
	# open files/initialize output flat files
	g1 = open('genomes.txt', 'a') #genomes table flat file
	r1 = open('replicons.txt', 'a') # replicons table flat file
	g2 = open('genes.txt', 'a') # genes table flat file
	x1 = open('extrefs.txt', 'a') #external refs table flat file
	e1 = open('exons.txt', 'a') # exons table flat file
	s1 = open('synonyms.txt', 'a') # gene synonyms table flat file
	f2 = open('functions.txt', 'a') # gene fns table flat file
	for line in f:
		line = line.rstrip()
		# open genbank file whose path is specified by line in file
		with gzip.open(line, 'r') as f1:
			# each file contains one genome, increment genome ct
			genome_id += 1
			# set local counter for number of replicons per genome
			num_replicons = 0
			# set local counter for number of cds per genome
			num_genes_g = 0
			# set local counter for genome size
			genome_size = 0
			# parse first record in genbank file for genome information
			for record in SeqIO.parse(f1, 'genbank'):
				# set local counter for number of genes per replicon
				num_genes_r = 0
				# increment replicon id
				replicon_id += 1
				num_replicons += 1
				# record replicon size
				repl_size = len(record)
				# increment genome size by length of replicon
				genome_size += repl_size
				# record genome tax_id 
				tax_id = record.features[0].qualifiers['db_xref'][0].split(':')[-1]
				# record genome name
				genome_name = record.annotations['source']
				# record genome domain
				domain = record.annotations['taxonomy'][0]
				# record genome assembly
				assembly = '-'
				for ref in record.dbxrefs:
					if re.search("Assembly", ref):
						assembly = ref.split(':')[-1] 
				# record replicon accession and date	
				gb_accession = record.name
				gb_date = record.annotations['date']
				# record replicon type and shape
				repl_type = '-' 
				if re.search("complete genome", record.description):
					repl_type = 'chromosome'
				elif re.search("chromosome", record.description):
					repl_type = 'chromosome'
				elif re.search("plasmid", record.description):
					repl_type = 'plasmid'	
				repl_shape = record.annotations['topology']
				for f in record.features:
					if f.type == 'CDS':
						# increment global and local gene counters
						gene_id += 1
						num_genes_g += 1
						num_genes_r += 1
						# get gene locus tag
						locus_tag = ', '.join(f.qualifiers['locus_tag'])
						# get protein id
						prot_id = '-'
						if 'protein_id' in f.qualifiers:
							prot_id = ', '.join(f.qualifiers['protein_id']) 
						# get gene name
						gene_name = '-'
						if 'gene' in f.qualifiers:
								gene_name = ', '.join(f.qualifiers['gene'])
						# get gene strand
						strand = 'NA'
						if f.strand == 1:
							strand = 'F'
						else:
							strand = 'R'
						# get number of exons
						num_exons = len(f.location.parts) 
						for e in xrange(1, num_exons+1):
							left = f.location.start
							right = f.location.end
							length = right - left + 1
							# write to exons file
							e1.write('\t'.join([str(gene_id), str(e), str(left), str(right), str(length)]) + '\n') 
						# get gene length
						gene_length = len(f)	
						# get gene product	
						product = '-'
						if 'product' in f.qualifiers:	
							product = ', '.join(f.qualifiers['product'])
						# get gene extrefs
						if 'db_xref' in f.qualifiers:
							refs_list = f.qualifiers['db_xref']
							for r in refs_list:
								r = r.split(':')
								xdb = r[0]
								xid = r[1]
								# write to external references file
								x1.write('\t'.join([str(gene_id), xdb, xid]) + '\n')
						# get gene functions
						fn = '-'
						if 'function' in f.qualifiers:
							fn = ', '.join(f.qualifiers['function'])
						# write to functions file
						f2.write('\t'.join([str(gene_id), fn]) + '\n')		
						# get gene synonyms
						if 'gene_synonym' in f.qualifiers: # if synonyms exist
							syn = ', '.join(f.qualifiers['gene_synonym'][0].split('; '))
						# write to synonyms file
						s1.write('\t'.join([str(gene_id), syn]) + '\n')	
						# write to genes file
						g2.write('\t'.join([str(gene_id), str(genome_id), str(replicon_id), locus_tag, str(prot_id),\
								gene_name, strand, str(num_exons), str(gene_length), product]) + '\n')
				# write to replicons file	 
				r1.write('\t'.join([str(replicon_id), str(genome_id), genome_name, repl_type, \
						repl_shape, str(num_genes_r), str(repl_size), gb_accession, gb_date]) + '\n') 	
			# write to genomes file
			g1.write('\t'.join([str(genome_id), genome_name, tax_id, domain, str(num_replicons),\
					str(num_genes_g), str(genome_size), assembly]) + '\n')
