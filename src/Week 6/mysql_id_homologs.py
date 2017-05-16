import MySQLdb

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="xxxxxx", db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
# make blast_511145 top hits table by selecting, for each gene, the hit in A.tumefaciens genome with the top bitscore
c.execute("""create table blast_511145_tophits select * from (select * from blast_511145 order by qseqid, bitscore desc) x group by qseqid;""")
# make blast_1435057 top hits table by selecting, for each gene, the hit in E.coli genome with the top bitscore
c.execute("""create table blast_1435057_tophits select * from (select * from blast_1435057 order by qseqid, bitscore desc) x group by qseqid;""")
# make two tables, both have the same content organized differently - created from querying both top hits tables above, returning the gene-hit pairs which showed up as top results in both
# queries 
c.execute("""create table homology_511145 select blast_511145_tophits.qseqid, blast_511145_tophits.sseqid from blast_511145_tophits inner join blast_1435057_tophits on (blast_511145_tophits.qseqid = blast_1435057_tophits.sseqid and blast_511145_tophits.sseqid = blast_1435057_tophits.qseqid);""")
c.execute("""create table homology_1435057 select blast_1435057_tophits.qseqid, blast_1435057_tophits.sseqid from blast_1435057_tophits inner join blast_511145_tophits on (blast_1435057_tophits.qseqid = blast_511145_tophits.sseqid and blast_1435057_tophits.sseqid = blast_511145_tophits.qseqid);""")
# show content from the homologs table for E.coli
c.execute("""select * from homology_511145""")
# capture and print as tab-sep table
hom1 = c.fetchall()
print "HOMOLOGY_511145"
for r in hom1:
	print r[0], '\t', r[1]
# show content from the homologs table for A.tumefaciens
c.execute("""select * from homology_1435057""")
hom2 = c.fetchall()
print "\nHOMOLOGY_1435057"
for r in hom2:
	print r[0], '\t', r[1]
