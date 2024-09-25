-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.feedback_id_seq;

CREATE SEQUENCE public.feedback_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.location_rating_id_seq;

CREATE SEQUENCE public.location_rating_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
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
	NO CYCLE;
-- DROP SEQUENCE public.user_contacts_id_seq;

CREATE SEQUENCE public.user_contacts_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.user_history_id_seq;

CREATE SEQUENCE public.user_history_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.feedback definition

-- Drop table

-- DROP TABLE public.feedback;

CREATE TABLE public.feedback (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	feedback text NOT NULL,
	stars int2 NULL,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT feedback_pkey PRIMARY KEY (id),
	CONSTRAINT feedback_stars_check CHECK (((stars >= 1) AND (stars <= 5)))
);


-- public.location_rating definition

-- Drop table

-- DROP TABLE public.location_rating;

CREATE TABLE public.location_rating (
	id serial4 NOT NULL,
	latitude numeric(10, 7) NOT NULL,
	longitude numeric(10, 7) NOT NULL,
	frequency int4 NOT NULL,
	rating int2 NULL,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT location_rating_pkey PRIMARY KEY (id),
	CONSTRAINT location_rating_rating_check CHECK (((rating >= '-5'::integer) AND (rating <= 5)))
);


-- public.police_auth_db definition

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
	latitude numeric(10, 3) NULL,
	longitude numeric(10, 3) NULL,
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
	latitude numeric(10, 3) NULL,
	longitude numeric(10, 3) NULL,
	CONSTRAINT user_auth_db_adhaar_number_key UNIQUE (aadhaar_number),
	CONSTRAINT user_auth_db_email_key UNIQUE (email),
	CONSTRAINT user_auth_db_phone_number_key UNIQUE (phone_number),
	CONSTRAINT user_auth_db_pkey PRIMARY KEY (id)
);


-- public.user_contacts definition

-- Drop table

-- DROP TABLE public.user_contacts;

CREATE TABLE public.user_contacts (
	id serial4 NOT NULL,
	aadhaar_number varchar(12) NOT NULL,
	"name" varchar(255) NOT NULL,
	relation varchar(100) NOT NULL,
	phone_number varchar(15) NOT NULL,
	email varchar(255) NOT NULL,
	status varchar(50) NOT NULL,
	priority int4 NULL,
	latitude numeric(9, 3) NULL,
	longitude numeric(9, 3) NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT user_contacts_phone_number_key UNIQUE (phone_number),
	CONSTRAINT user_contacts_pkey PRIMARY KEY (id),
	CONSTRAINT user_contacts_priority_check CHECK (((priority >= 0) AND (priority <= 5))),
	CONSTRAINT user_contacts_aadhaar_number_fkey FOREIGN KEY (aadhaar_number) REFERENCES public.user_auth_db(aadhaar_number)
);


-- public.user_history definition

-- Drop table

-- DROP TABLE public.user_history;

CREATE TABLE public.user_history (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	"source" varchar(255) NOT NULL,
	destination varchar(255) NOT NULL,
	"path" jsonb NOT NULL,
	rating int2 NULL,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT user_history_pkey PRIMARY KEY (id),
	CONSTRAINT user_history_rating_check CHECK (((rating >= 1) AND (rating <= 5))),
	CONSTRAINT user_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_auth_db(id)
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