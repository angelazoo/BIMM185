--Script makes series of tables in MySQL which comprise a relational
--database for gene/CDS information parsed from Genbank formatted files

/*
Creates genomes table to hold genome_id (pri), taxonomy_id, genome short/long
names, size in base pairs, domain, and accession and release date, all
parsed from Genbank record for the genome
*/
create table genomes (
	genome_id int(10) unsigned not null,
	genome_name varchar(100) not null,
	tax_id int(10) unsigned not null,
	domain enum('bacteria','archaea','eukarya') not null,
	num_replicons int(10) unsigned not null,
	num_genes int(10) unsigned not null,	
	size_bp int(10) unsigned not null,
	assembly varchar(100) not null,
	primary key (genome_id),
	key (tax_id)
) engine=InnoDB;

/*
Creates replicons table to hold replicon_id (pri), genome_id (for), name, 
num_genes, replicon type and replicon structure, all parsed from Genbank
record for the replicon 
*/
create table replicons (
	replicon_id int(10) unsigned not null,
	genome_id int(10) unsigned not null,
	name varchar(100) not null,
	replicon_type enum('chromosome','plasmid') not null,
	replicon_structure enum('linear','circular') not null,
	num_genes int(10) unsigned not null,
	len_bp int(10) unsigned not null,
	gb_accession varchar(50) not null,
	gb_release_date varchar(50) not null,
	primary key (replicon_id),
	key (genome_id)
) engine=InnoDB;

/*
Creates genes table to hold gene_id (pri), genome_id (for), replicon_id (for),
locus_tag, gene name, strand, number of exons, len in bp, product name, all
parsed from Genbank feature for the gene 
*/
create table genes (
	gene_id int(10) unsigned not null,
	genome_id int(10) unsigned not null,
	replicon_id int(10) unsigned not null,
	locus_tag varchar(25) not null,
	prot_id varchar(25) not null,	
	name varchar(100) not null,
	strand varchar(5) not null,
	num_exons int(10) unsigned not null,
	len_bp int(10) unsigned not null,
	product varchar(250) not null,
	primary key (gene_id),
	key (genome_id),
	key (replicon_id)
) engine=InnoDB;

/*
Creates exons table to hold gene_id, exon number, left pos, right pos,
length in bp, parsed from Genbank feature for the gene 
*/
create table exons (
	gene_id int(10) unsigned not null,
	exon int(10) unsigned not null,
	left_pos int(10) unsigned not null,
	right_pos int(10) unsigned not null,
	length int(10) unsigned not null
) engine=InnoDB;

/*
Creates synonyms table to hold gene_id (pri), and synonyms, parsed from 
Genbank feature for the gene 
*/
create table synonyms (
	gene_id int(10) unsigned not null,
	synonyms varchar(200) not null,
	primary key (gene_id)
) engine=InnoDB;

/*
Creates ext references table to hold gene_id, external dbs, and ext id,
one line per external reference available for gene, all parsed from Genbank
feature for the gene 
*/
create table extrefs (
	gene_id int(10) unsigned not null,
	ext_db varchar(100) not null,
	ext_id varchar(100) not null
) engine=InnoDB;

/*
Creates functions table to hold gene_id and functions, all parsed from Genbank
feature for the gene 
*/
create table functions (
	gene_id int(10) unsigned not null,
	functions varchar(250) not null,
	primary key (gene_id)
) engine=InnoDB; 
