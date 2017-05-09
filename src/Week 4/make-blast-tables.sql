--Script makes blast_genome table in MySQL

create table blast_511145 (
	qseqid varchar(25) not null,
	sseqid varchar(25) not null,
	qlen int(10) unsigned not null,
	slen int(10) unsigned not null,
	bitscore float(7,4) unsigned not null,
	evalue float(7,4) unsigned not null,
	pident float(7,4) unsigned not null,
	nident int(10) unsigned not null,
	length int(10) unsigned not null,
	qcovs int(10) unsigned not null,
	qstart int(10) unsigned not null,
	qend int(10) unsigned not null,
	sstart int(10) unsigned not null,
	send int(10) unsigned not null,		
	scov float(7,4) unsigned not null
) engine=InnoDB;

