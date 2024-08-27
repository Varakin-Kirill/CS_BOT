-- psql postgres://postgres:cs_hookah@localhost:5432/cs
create table
    if not exists users (
        user_id uuid not null primary key,
        tg_id int not null,
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
        user_id uuid not null references users (user_id),
        amount int not null,
        datetime timestamp not null,
        ps boolean not null,
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

"""SELECT COUNT(*) as res FROM items_purchased 
    WHERE item_id < 5
    AND created_at >= date_trunc('month', now())
    AND created_at < date_trunc('month', now()) + interval '1 month',
    GROUP BY master;



    """ CREATE TYPE expense_type AS ENUM (
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
        comment text null
    );

create table
    if not exists duties (
        id serial primary key,
        master uuid not null references masters (user_id),
        opened_at timestamp not null default now (),
        closed_at timestamp null
    );

insert into
    items (name, price)
values
    ('Вечерний', 700);

insert into
    items (name, price)
values
    ('Дневной', 550);

insert into
    items (name, price)
values
    ('Постоялец', 550);

insert into
    items (name, price)
values
    ('Постоялец Супер', 500);

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