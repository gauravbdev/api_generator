/*
truncate table products;
truncate table orders;
truncate table ordered_products;
truncate table customers;
*/

insert into products(name, category, price, available_qty, description)
(
	select 'iPhone', 'phone', 700.0, 100, 'smartphone by apple'
	union 
	select 'audio technica headphone', 'audio', 150, 10, 'high quality headphones'
	union
	select 'logitech wireless mouse', 'computer accessories', 30, 100, 'wireless mouse by logitech'
);

insert into customers(first_name, last_name, address, city, state, zip_code, email, phone)
(
	select 'jon', 'doe', '1 infinite loop', 'cupertino', 'CA', '12345', 'jon.doe@apple.com', '3434323232'
	UNION
	select 'nick', 'wilson', '123 23rd street', 'new york', 'NY', '353543', 'nick.wilson@wilson.com', '35353429'
);

insert into orders(customer_id, created_datetime, is_paid)
(
	select 1, 1566621500, true
	union
	select 1, 1566621515, false
);

insert into ordered_products(order_id, product_id, qty)
(
	select 1, 1, 1
	union
	select 1, 2, 1
	union 
	select 1, 3, 2
	union 
	select 2, 3, 1
);	

insert into ordered_products2(order_id, product_id, qty)
(
	select 1, 1, 1
	union
	select 1, 2, 1
	union 
	select 1, 3, 2
	union 
	select 2, 3, 1
);	
