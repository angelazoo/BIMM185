import MySQLdb

#connect to mysql
db=MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="azou", passwd="Gougou12", db="azou_db")
# define cursor object from which to execute queries
c=db.cursor()
c.execute("""create table if not exists hnscc_clinical (pat_id varchar(12) not null, hpv enum('Negative', 'Positive') not null, smoking_history varchar(25) not null, pack_years varchar(25) not null, alcohol_history varchar(25) not null, num_drinks varchar(25) not null, key(pat_id)) engine=innodb;""") 
c.execute("""load data local infile '/home/linux/ieng6/bm185s/azou/Final-project/hnscc-clinical-collated.txt' into table hnscc_clinical (pat_id, hpv, smoking_history, pack_years, alcohol_history, num_drinks);""")
