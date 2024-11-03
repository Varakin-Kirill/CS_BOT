-- psql postgres://postgres:cs_hookah@localhost:5432/cs
truncate items_purchased




create table
    if not exists users (
        tg_id int not null unique,
        name text not null,
        surname text not null,
        phone text not null
    );

create table
    if not exists masters (
        user_id uuid primary key,
        tg_id int not null,
        name text not null,
        surname text not null,
        phone text not null
    );

insert into
    masters
values
    (
        '9e61fbc2-8e9b-4e8f-ae85-8a5ca29f9488',
        906936941,
        'Nick',
        'Shrek',
        'aga'
    ),
    (
        'ef9e34a4-eb25-4129-81e7-0b5581a77940',
        1058326905,
        'Костя',
        'Горелыч',
        'хз'
    ),
    (
        'af3342ae-ce93-46f4-b1d2-a6ec4c6ba06c',
        829192290,
        'Кир',
        'Великий',
        'Потом заполним'
    );

create table
    if not exists reservations (
        id serial primary key,
        user_tg_id int not null references users (tg_id),
        amount int not null,
        datetime timestamp not null,
        comment text,
        success boolean not null default false
    );

create table
    if not exists items (
        item_id serial primary key,
        name text not null,
        price int not null
    );

CREATE TYPE payment_type AS ENUM ('cash', 'transfer');

create table
    if not exists items_purchased (
        created_at timestamp not null default now (),
        master uuid not null references masters (user_id),
        item_id int not null references items (item_id),
        payment payment_type not null,
        amount int not null,
        comment text not null
    );

 CREATE TYPE expense_type AS ENUM (
    'tobacco',
    'coal',
    'drinks',
    'rent',
    'salary',
    'other'
);

create table
    if not exists expenses (
        id serial primary key,
        expense expense_type not null,
        amount int not null, -- final price
        comment text not null, 
        datetime timestamp not null
    );

create table
    if not exists duties (
        id serial primary key,
        master uuid not null references masters (user_id),
        opened_at timestamp not null default now (),
        closed_at timestamp null,
        salary int
    );

with duty as (select * from duties where id = 6)
SELECT count(*) as hookahs from items_purchased  
    where item_id <5  
    and created_at >= (select opened_at from duty) 
    and created_at < (select closed_at from duty)
    and master = (select master from duty)

CREATE OR REPLACE FUNCTION count_salary() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary is not NUll then RETURN NULL; end if;
    with ts as(SELECT count(*) as hookahs from items_purchased  
    where item_id <5  
    and created_at >= NEW.opened_at 
    and created_at < NEW.closed_at
    and master = NEW.master)
    UPDATE "duties"
    SET salary = (select greatest(1250, hookahs * 100 + 250) as salary from ts) where id = NEW.id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER salary_count
After update ON duties
FOR EACH ROW
EXECUTE FUNCTION count_salary();

create table
    if not exists presets (
        id      serial  primary key,
        user_id UUID    not null,
        item_id int     not null,
        comment text    not null
    );

insert into
    items (name, price)
values
    ('Вечерний', 800);

insert into
    items (name, price)
values
    ('Дневной', 600);

insert into
    items (name, price)
values
    ('Постоялец', 600);

insert into
    items (name, price)
values
    ('Постоялец Супер', 550);

insert into
    items (name, price)
values
    ('Напиток 100', 100);

insert into
    items (name, price)
values
    ('Напиток 150', 150);

insert into
    items (name, price)
values
    ('Чай', 200);


    SELECT SUM(salary) FROM duties
    WHERE opened_at >= DATE_TRUNC('month', CURRENT_DATE)
    AND closed_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
    GROUP BY master





-- скрипт для подсчета прибыли
SELECT 
    income_subquery.total_income,
    expenses_subquery.expenses,
    (income_subquery.total_income - expenses_subquery.expenses) AS clear_income
FROM 
    (SELECT 
         SUM(items.price) AS total_income
     FROM 
         items_purchased
     LEFT JOIN 
         items ON items.item_id = items_purchased.item_id
     WHERE 
         items_purchased.created_at < NOW()
         AND items_purchased.created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
    ) AS income_subquery,
    (SELECT 
         SUM(amount) AS expenses
     FROM 
         expenses
     WHERE 
         datetime < NOW()
         AND datetime >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
    ) AS expenses_subquery;
