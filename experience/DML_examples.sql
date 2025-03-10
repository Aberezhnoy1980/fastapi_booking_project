SELECT * FROM hotels;

insert into hotels (title, location) 
values ('Житомир Агра резорт 15 звезд','ул. Красивая, стрение 13/б')
returning hotels.id;

update hotels set title = 'Агра резорт 15 звезд', location = 'Житомир ул. Красивая, стрение 13/б' where id = 10;

select id, title, location from hotels;

insert into hotels (title, location)
values ('Отель 5 звезд у игоря', 'Сочиб ул. Морская, 7')

# Операции чтения нет необходимости комитить, в отличии от операций записи, где необходимо фикссировать изменения

select id, title, location
from hotels
--where id = 1 and title = 'Хотел 5 старс'
limit 5
offset 0
;

# Варианты для проверки вхождения подстроки

select id, title, location 
from hotels
where title ilike '%хостел%';

select * from hotels where position('Хостел' in title) > 0;

select * from hotels where title ~* 'Хостел';

# Смотрим кодировку

SHOW SERVER_ENCODING;

select datname, pg_encoding_to_char(encoding) from pg_database;

--SET client_encoding = 'UTF8';
--UPDATE pg_database SET datcollate='ru_RU.UTF-8', datctype='ru_RU' WHERE datname='booking';
--UPDATE pg_database set encoding = pg_char_to_encoding('UTF8') where datname = 'booking';

select id, title, lower(location) from hotels;


-- contains in sqlalchemy
SELECT hotels.id, hotels.title, hotels.location 
FROM hotels 
WHERE (hotels.location LIKE '%' || 'Мег' || '%') 
LIMIT 5 OFFSET 0


-- icontains in sqlalchemy
SELECT hotels.id, hotels.title, hotels.location 
FROM hotels 
WHERE (hotels.location ILIKE '%' || 'мег' || '%') 
LIMIT 5 OFFSET 0


SELECT hotels.id, hotels.title, hotels.location 
FROM hotels 
WHERE (lower(hotels.title) LIKE '%' || 'хост' || '%') 
LIMIT 5 OFFSET 0

INSERT INTO hotels (title, location) VALUES ('Уютный дворик', 'Мегион, ул. Геологоразведчиков, 19') RETURNING hotels.id, hotels.title, hotels.location;

INSERT INTO hotels (title, location) VALUES ('Поля', 'Краснодар, ул. Петра Метальникова, 1') RETURNING hotels.id, hotels.title, hotels.location;

delete from hotels where id > 17;

