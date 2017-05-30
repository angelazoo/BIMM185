import MySQLdb

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="Gougou12", db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
# make blast_511145 top hits table by selecting, for each gene, the hit in A.tumefaciens genome with the top bitscore
c.execute("""create table if not exists blast_511145_tophits select * from (select * from blast_511145 where qcovs>=60 or scov>=0.6 order by qseqid, bitscore desc) x group by qseqid;""")
# make blast_1435057 top hits table by selecting, for each gene, the hit in E.coli genome with the top bitscore
c.execute("""create table if not exists blast_1435057_tophits select * from (select * from blast_1435057 where qcovs>=60 or scov>=0.6 order by qseqid, bitscore desc) x group by qseqid;""")
# make two tables, both have the same content organized differently - created from querying both top hits tables above, returning the gene-hit pairs which showed up as top results in both
# queries 
c.execute("""select blast_511145_tophits.qseqid, blast_511145_tophits.sseqid from blast_511145_tophits inner join blast_1435057_tophits on (blast_511145_tophits.qseqid = blast_1435057_tophits.sseqid and blast_511145_tophits.sseqid = blast_1435057_tophits.qseqid);""")
# capture and print as tab-sep table
hom1 = c.fetchall()
with open("mysql_homologs-out.txt", 'w') as f:
		for r in hom1:
			f.write('\t'.join([r[0], r[1],"orthology", "BDBH"])+'\n')
c.execute("""create table if not exists homology (gid_1 varchar(15) not null, gid_2 varchar(15) not null, type enum('orthology', 'paralogy', 'xenology', 'homology') not null, method enum('bdbh', 'ohtp', 'topblasthit', 'sigblast') not null, key (gid_1), key(gid_2)) engine=innodb;""") 
c.execute("""load data local infile '/home/linux/ieng6/bm185s/azou/Week6/mysql_homologs-out.txt' into table homology (gid_1, gid_2, type, method);""")
