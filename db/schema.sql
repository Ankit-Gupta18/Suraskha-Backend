-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.police_auth_db_id_seq;

CREATE SEQUENCE public.police_auth_db_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.user_auth_db_id_seq;

CREATE SEQUENCE public.user_auth_db_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.police_auth_db definition

-- Drop table

-- DROP TABLE public.police_auth_db;

CREATE TABLE public.police_auth_db (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	police_id varchar(50) NOT NULL,
	police_station_address varchar(255) NOT NULL,
	phone_number varchar(15) NOT NULL,
	email varchar(255) NOT NULL,
	id_card bytea NULL,
	avatar bytea NULL,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT police_auth_db_email_key UNIQUE (email),
	CONSTRAINT police_auth_db_phone_number_key UNIQUE (phone_number),
	CONSTRAINT police_auth_db_pkey PRIMARY KEY (id),
	CONSTRAINT police_auth_db_police_id_key UNIQUE (police_id)
);

-- Table Triggers

create trigger update_police_auth_timestamp before
update
    on
    public.police_auth_db for each row execute function update_timestamp();


-- public.user_auth_db definition

-- Drop table

-- DROP TABLE public.user_auth_db;

CREATE TABLE public.user_auth_db (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	aadhaar_number varchar(12) NOT NULL,
	state varchar(100) NULL,
	age_group varchar(20) NULL,
	gender varchar(10) NULL,
	phone_number varchar(15) NOT NULL,
	email varchar(255) NOT NULL,
	avatar bytea NULL,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT user_auth_db_adhaar_number_key UNIQUE (aadhaar_number),
	CONSTRAINT user_auth_db_email_key UNIQUE (email),
	CONSTRAINT user_auth_db_phone_number_key UNIQUE (phone_number),
	CONSTRAINT user_auth_db_pkey PRIMARY KEY (id)
);



-- DROP FUNCTION public.update_timestamp();

CREATE OR REPLACE FUNCTION public.update_timestamp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$function$
;