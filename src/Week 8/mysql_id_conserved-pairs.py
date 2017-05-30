import MySQLdb

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="xxxxxxx", db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
c.execute("""create table if not exists genes_pos select genes.gene_id, genes.genome_id, genes.replicon_id, genes.locus_tag, genes.prot_id, genes.name, genes.strand, exons_2.left_pos, exons_2.right_pos from genes inner join exons_2 on (genes.gene_id = exons_2.gene_id);""")
# open flat file containing homolog pairs
with open("mysql_homologs-out.txt", 'r') as f:
	# for each pair of homologs
	for line in f:
		line = line.rstrip().split('\t')
		# prot id for ecoli
		gid_1 = line[0]
		# prot id for A. tumefaciens
		gid_2 = line[1].rstrip()
		# find ecoli gene info corresponding to ecoli prot
		c.execute("""select * from genes_pos where genes_pos.prot_id="{}";""".format(gid_1))
		gid_1_pos = c.fetchone()
		# find all genes within 5 genes distance upstream of conserved gene in ecoli genome, on the same replicon and the same strand
		c.execute("""select * from genes_pos where genes_pos.gene_id<{} and genes_pos.genome_id={} and genes_pos.replicon_id={} and genes_pos.prot_id != '-' and genes_pos.strand="{}" order by left_pos desc limit 6;""".format(gid_1_pos[0], gid_1_pos[1], gid_1_pos[2], gid_1_pos[6]))
		# save neighbors protein names to list
		g1_n = [r[4] for r in c.fetchall()]
		# find all genes within 5 genes distance downstream of conserved gene in ecoli genome, on the same replicon and the same strand
		c.execute("""select * from genes_pos where genes_pos.gene_id>{} and genes_pos.genome_id={} and genes_pos.replicon_id={} and genes_pos.prot_id != '-' and genes_pos.strand="{}" limit 6;""".format(gid_1_pos[0], gid_1_pos[1], gid_1_pos[2], gid_1_pos[6]))
		# append neighbor protein names to list
		g1_n.extend([r[4] for r in c.fetchall()])
		# find tumefaciens gene info corresponding to homologous tumefaciens prot
		c.execute("""select * from genes_pos where genes_pos.prot_id="{}";""".format(gid_2))
		gid_2_pos = c.fetchone()
		# find all genes within 5 genes distance upstream of conserved gene in tumefaciens genome, on the same replicon and the same strand
		c.execute("""select * from genes_pos where genes_pos.gene_id<{} and genes_pos.genome_id={} and genes_pos.replicon_id={} and genes_pos.prot_id != '-' and genes_pos.strand="{}" order by left_pos desc limit 6;""".format(gid_2_pos[0], gid_2_pos[1], gid_2_pos[2], gid_2_pos[6]))
		# save neighbors protein names to list
		g2_n = [r[4] for r in c.fetchall()]
		# find all genes within 5 genes distance downstream of conserved gene in tumefaciens genome, on the same replicon and the same strand
		c.execute("""select * from genes_pos where genes_pos.gene_id>{} and genes_pos.genome_id={} and genes_pos.replicon_id={} and genes_pos.prot_id != '-' and genes_pos.strand="{}" limit 6;""".format(gid_2_pos[0], gid_2_pos[1], gid_2_pos[2], gid_2_pos[6]))
		# append neighbor protein names to list
		g2_n.extend([r[4] for r in c.fetchall()])
		# for each ecoli neighbor in the list	
		for i in xrange(0, len(g1_n)):
			# if there is a valid protein (redundant check as query before excludes all non-protein-coding genes) 
			if g1_n[i] != '-':
				# query for homologous tumefaciens protein in homology table 
				c.execute("""select gid_2 from homology where homology.gid_1="{}";""".format(g1_n[i]))
				# if no query, then do nothing (move on to next)
				if not c.rowcount:
					pass
				# if tumefaciens homolog exists
				else:
					# fetch protein name of the homolog
					h1 = c.fetchone()[0]
					# check if this homolog is listed as a neighbor in the tumefaciens list of neighbor proteins
					for j in xrange(0, len(g2_n)):
						# if there is a match
						if h1 == g2_n[j]:
							# get name of ecoli locus tag corresponding to ecoli protein
							gene_1 = gid_1_pos[3]
							# get name of ecoli locus tag corresponding to ecoli neighbor protein
							c.execute("""select locus_tag from genes_pos where prot_id="{}";""".format(g1_n[i]))
							gene_2 = c.fetchone()[0]
							# print original conserved protein and neighbor conserved ecoli protein+info in tab sep format 
							print '\t'.join([gene_1, gene_2])  
