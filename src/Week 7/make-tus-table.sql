--Script makes blast_genome table in MySQL

create table tus (
    gid_1 varchar(10) not null,
    gid_2 varchar(10) not null,
    distance int(10) unsigned not null,
    status enum('TP', 'TN') not null,
    prob double precision not null,
    key (gid_1),
    key (gid_2)
) engine=InnoDB;

