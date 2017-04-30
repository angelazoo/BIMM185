from Bio import SeqIO
import gzip, sys

'''
Script opens zipped genbank file and parses each CDS feature within the file, printing tax_id, accession,
start, end, strand, gene name, locus tag, gene synonyms, protein name, EC number(s) and external references
for each CDS as tab-separated output
'''

# open zipped genbank file (path specified by cmd line argument
with gzip.open(sys.argv[1], 'r') as f:
	# print header line for output
	print '\t'.join(['Tax ID', 'Accession', 'Start', 'End', 'Strand', 'Gene Name', 'Locus Tag', 'Synonyms', 'Protein Name', 'EC Number(s)', 'External References'])
	# parse each record in genbank file	
	for record in SeqIO.parse(f, 'genbank'):
		# retrieve tax_id for the record
		tax_id = record.features[0].qualifiers['db_xref'][0].split(':')[-1]
		# iterate through record features (e.g. genes)
		for gene in record.features:
			# check if feature is CDS
			if gene.type == 'CDS':
				# retrieve protein id
				prot_id = '-'
				if 'protein_id' in gene.qualifiers: # if protein_id exists
					prot_id = ', '.join(gene.qualifiers['protein_id'])
				# retrieve CDS start/end coordinates
				start = str(gene.location.start)
				end = str(gene.location.end)
				# retrieve CDS strand
				strand = str(gene.location.strand)
				# retrieve CDS gene name
				gene_name = '-'
				if 'gene' in gene.qualifiers: # if gene name exists
					gene_name = ', '.join(gene.qualifiers['gene'])
				# retrieve locus tag
				locus = '-'
				if 'locus_tag' in gene.qualifiers: # if locus tag exists
					locus = ', '.join(gene.qualifiers['locus_tag'])
				# retrieve gene synonym 
				syn = '-'
				if 'gene_synonym' in gene.qualifiers: # if synonyms exist
					syn = ', '.join(gene.qualifiers['gene_synonym'][0].split('; '))
				# retrieve protein name
				prot_name = '-'
				if 'product' in gene.qualifiers: # if protein name exists
					prot_name = ', '.join(gene.qualifiers['product'])
				# retrieve EC numbers
				ec = '-'	
				if 'EC_number' in gene.qualifiers: # if ec number exists
					ec = ', '.join(gene.qualifiers['EC_number'])
				# external references
				ext_ref = '-'
				if 'db_xref' in gene.qualifiers:
					ext_ref = ', '.join(gene.qualifiers['db_xref'])
				# print all fields for CDS as tab-separated line
				print '\t'.join([tax_id, prot_id, start, end, strand, gene_name, locus, syn, prot_name, ec, ext_ref])		
		
