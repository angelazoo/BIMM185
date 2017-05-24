import MySQLdb

# connect to mysql server
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="Gougou12", db="azou_db")
# create cursor object to execute commands on db
c=db.cursor()
# create operons table with operon name, gene name, loc_tag fields
c.execute("""create table if not exists operons (operon varchar(80) not null, gname varchar(50) not null, loc_tag varchar(25) not null) engine=InnoDB""")
# load operon_genes.txt flat file into operons table in MySQL
c.execute("""load data local infile '/home/linux/ieng6/bm185s/azou/Week6/operon_genes.txt' into table operons (operon, gname, loc_tag)""")
# create second exons table containing one start/stop pos per gene
c.execute("""create table if not exists exons_2 select * from (select * from exons order by gene_id, exon) x group by gene_id;""")
# create genes_pos table based on inner join of genes and exons table
c.execute("""create table if not exists genes_pos select genes.gene_id, genes.locus_tag, genes.prot_id, genes.name, genes.strand, exons_2.left_pos, exons_2.right_pos from genes inner join exons_2 on (genes.gene_id = exons_2.gene_id);""")
# create genes_operons table based on inner join of genes_pos and operons table which only
# contains data for genes known to be located in an operon
c.execute("""create table if not exists genes_operons select * from genes_pos inner join operons on (genes_pos.locus_tag = operons.loc_tag);""")
# create table allgenes_operons based on left join of genes_pos and operons table which
# contains data for all genes in genome (operon name = none for genes not in operons)
c.execute("""create table allgenes_operons select * from genes_pos left join operons on (genes_pos.locus_tag = operons.loc_tag);""")
# write genes_operons table to flat file
c.execute("""select * from genes_operons""")
g_o = c.fetchall()
for r in g_o:
	print '\t'.join(str(e) for e in r)
# write allgenes_operons table to flat file
c.execute("""select * from allgenes_operons order by gene_id;""")
g_o = c.fetchall()
for r in g_o:
    print '\t'.join(str(e) for e in r)
