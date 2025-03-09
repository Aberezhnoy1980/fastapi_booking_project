create temporary table test1(
	id int
);

create temporary table test2(
	id int
);

start transaction;
insert into test1 (id) values (35);
insert into test1 (id) values (1 / 0);
insert into test2 (id) values (255);
end transaction;


select * from test1;
select * from test2;