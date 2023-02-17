DROP SCHEMA IF EXISTS cyberhire CASCADE;

CREATE SCHEMA IF NOT EXISTS cyberhire;

-- Create the user table
CREATE TABLE IF NOT EXISTS cyberhire."user" (
	id serial4 NOT NULL,
	username varchar(100) NOT NULL,
	"password" varchar(100) NOT NULL,
	email varchar(50) NOT NULL,
	is_recruiter bool NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id),
	CONSTRAINT user_email_unique_2 UNIQUE (email),
	CONSTRAINT user_username_unique_1 UNIQUE (username)
);

-- Create the user profile table
CREATE TABLE IF NOT EXISTS cyberhire."user_profile" (
	user_id int4 NOT NULL PRIMARY KEY,
	first_name varchar(30) NOT NULL,
	last_name varchar(30) NOT NULL,
	profile_picture bytea NULL,
	resume byteA NULL,
	CONSTRAINT user_profile_fk FOREIGN KEY (user_id) REFERENCES cyberhire.user (id)
);

-- Create the skill table
CREATE TABLE IF NOT EXISTS cyberhire."skill" (
	id serial4 NOT NULL PRIMARY KEY,
	skill varchar(30) NOT NULL UNIQUE
);

-- Create the user_profile_skill 
CREATE TABLE IF NOT EXISTS cyberhire.user_profile_skill (
	user_profile_id int4 NOT NULL,
	skill_id int4 NOT NULL,
	CONSTRAINT user_profile_skill_user_profile_fk FOREIGN KEY (user_profile_id) REFERENCES cyberhire.user_profile (user_id),
	CONSTRAINT user_profile_skill_skill_fk2 FOREIGN KEY (skill_id) REFERENCES cyberhire.skill (id),
	CONSTRAINT user_profile_skill_unique UNIQUE (user_profile_id, skill_id)
);