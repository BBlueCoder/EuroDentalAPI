CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    profile_name varchar(25) not null unique
);

create table rights (
	 id SERIAL PRIMARY KEY,
	 right_name varchar(50),
	 is_given boolean ,
	 profile_id int not null unique ,
	 FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number varchar(10),
    profile_id int not null unique ,
	FOREIGN KEY (profile_id) REFERENCES profiles(id),
	is_blocked boolean 
);
CREATE INDEX idx_email ON users(email);

CREATE TABLE public.clients (
	id serial4 NOT NULL,
	email varchar(255) NOT NULL,
	first_name varchar(100) NULL,
	last_name varchar(100) NULL,
	phone_number varchar(10) NULL,
	image_path varchar NULL,
	address text NULL,
	city varchar NULL,
	fixed_phone_number varchar NULL,
	description varchar NULL,
	CONSTRAINT clients_email_key UNIQUE (email),
	CONSTRAINT clients_pkey PRIMARY KEY (id)
);

create table tasks (
	id BIGSERIAL PRIMARY KEY,
	task_name varchar(50),
	task_type varchar(50),
	description text,
	status varchar(50) not null,
	technician_id int not null ,
	FOREIGN KEY (technician_id) REFERENCES users(id) ,
	create_by int not null ,
	FOREIGN KEY (create_by) REFERENCES users(id) ,
	client_id int not null ,
	FOREIGN KEY (client_id) REFERENCES clients(id)
);

create table categories(
	id SERIAL PRIMARY KEY,
	category varchar(50)
);

create table sub_categories(
	id SERIAL PRIMARY KEY,
	sub_category varchar(50),
	category_id int not null,
	FOREIGN KEY (category_id) REFERENCES categories(id)
);

create table products(
	id SERIAL PRIMARY KEY,
	product_name varchar(100),
	brand varchar(50),
	id_categorie int,
	foreign key(id_categorie) references categories(id),
	id_sub_categorie int,
	foreign key(id_sub_categorie) references sub_categories(id),
	price float,
	stock_quantity int,
	has_warranty boolean ,
	warranty_duration_months int,
	purshase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	description varchar 
);

create table task_products (
	id bigSERIAL PRIMARY KEY,
	product_id int,
	FOREIGN KEY (product_id) REFERENCES products(id) ,
	quantity int,
	task_id int,
	FOREIGN KEY (task_id) REFERENCES tasks(id) ,
	purshase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

create table invoices (
	id bigSERIAL PRIMARY KEY,
	client_id int ,
	FOREIGN KEY (client_id) REFERENCES clients(id) ,
	task_id int ,
	FOREIGN KEY (task_id) REFERENCES tasks (id) ,
	bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
	amount_paid float ,
	is_paid boolean 
);

create table purshases (
	id bigSERIAL PRIMARY KEY,
	product_id int,
	FOREIGN KEY (product_id) REFERENCES products(id) ,
	quantity int,
	purshase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	client_id int ,
	FOREIGN KEY (client_id) REFERENCES clients(id),
	invoice_id int,
	FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);


SELECT datname, 
       has_database_privilege('api_app', datname, 'CONNECT') AS can_connect,
       has_database_privilege('api_app', datname, 'CREATE') AS can_create,
       has_database_privilege('api_app', datname, 'TEMP') AS can_temp
FROM pg_database
WHERE datname = 'eurodental';

SELECT table_schema,
       table_name,
       privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'api_app';

