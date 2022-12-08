CREATE TABLE IF NOT EXISTS cyberhire."user" (
	id serial4 NOT NULL,
	username varchar(100) NOT NULL,
	"password" varchar(100) NOT NULL,
	email varchar(50) NOT NULL,
	isrecruiter bool NOT NULL,
	CONSTRAINT user_email_unique_2 UNIQUE (email),
	CONSTRAINT user_pkey PRIMARY KEY (id),
	CONSTRAINT user_username_unique_1 UNIQUE (username)
)