/*
drop table if exists products;
drop table if exists orders;
drop table if exists customers;
drop table if exists ordered_products;
*/

create table products
(
	product_id serial primary key,
	name varchar,
	category varchar,
	price numeric(20,6),
	available_qty int,
	description text
);

create table orders
(
	order_id serial primary key,
	customer_id int,
	created_datetime bigint,
	is_paid boolean
	
);

create table ordered_products
(
	order_id int,
	product_id int,
	qty int
);


create table ordered_products2
(
	order_id int,
	product_id int,
	qty int,
	primary key(order_id, product_id)
);

create table customers
(
	customer_id serial primary key,
	first_name varchar,
	last_name varchar,
	address text,
	city varchar,
	state varchar,
	zip_code varchar,
	email varchar,
	phone varchar
);

