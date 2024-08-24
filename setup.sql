create table if not exists users (
    user_id     uuid    not null primary key,
    tg_id       int     not null,
    name        text    not null,
    surname     text    not null,
    phone       text    not null
);

create table if not exists masters (
    user_id     uuid    primary key,
    tg_id       int     not null,
    name        text    not null,
    surname     text    not null,
    phone       text    not null
);

create table if not exists reservations (
    id          serial      primary key,
    user_id     uuid        not null references users(user_id),
    amount      int         not null,
    datetime    timestamp   not null,
    ps          boolean     not null,
    success     boolean     not null default false
);

CREATE TYPE payment_type AS ENUM ('cash', 'transfer');

create table if not exists items (
    item_id     serial  primary key,
    name        text    not null,
    price       int     not null
);

create table if not exists items_purchased (
    created_at      timestamp   not null default now(),
    master          uuid        not null references masters(user_id),
    item_id         int         not null references items(item_id),
    amount          int         not null
);

CREATE TYPE expense_type AS ENUM ('tobacco', 'coal', 'drinks', 'rent', 'salary', 'other');

create table if not exists expenses (
    id          serial          primary key,
    expense     expense_type    not null,
    amount      int             not null,  -- final price
    comment     text                null
);

create table if not exists duties (
    id          serial          primary key,
    day         date            not null default now() unique,
    master      uuid            not null references masters(user_id)
);

insert into items (name, price) values ('Вечерний', 700);
insert into items (name, price) values ('Дневной', 550);
insert into items (name, price) values ('Постоялец', 550);
insert into items (name, price) values ('Постоялец Супер', 500);
insert into items (name, price) values ('Напиток 100', 100);
insert into items (name, price) values ('Напиток 150', 150);
insert into items (name, price) values ('Чай', 200);