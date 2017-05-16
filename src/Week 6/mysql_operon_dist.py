import MySQLdb

db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="Gougou12", db="azou_db")
c=db.cursor()
c.execute("""create table if not exists operons (operon varchar(80) not null, gname varchar(50) not null, loc_tag varchar(25) not null) engine=InnoDB""")
c.execute("""load data local infile '/home/linux/ieng6/bm185s/azou/Week6/operon_genes.txt' into table operons (operon, gname, loc_tag)""")
c.execute("""create table if not exists exons_2 select * from (select * from exons order by gene_id, exon) x group by gene_id;""")
c.execute("""create table if not exists genes_pos select genes.gene_id, genes.locus_tag, genes.prot_id, genes.name, genes.strand, exons_2.left_pos, exons_2.right_pos from genes inner join exons_2 on (genes.gene_id = exons_2.gene_id);""")
c.execute("""create table if not exists genes_operons select * from genes_pos inner join operons on (genes_pos.locus_tag = operons.loc_tag);""")
c.execute("""select * from genes_operons""")
g_o = c.fetchall()
for r in g_o:
	print '\t'.join(str(e) for e in r)
