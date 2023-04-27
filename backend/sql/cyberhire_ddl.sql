DROP SCHEMA IF EXISTS cyberhire CASCADE;

CREATE SCHEMA IF NOT EXISTS cyberhire;

SET SEARCH_PATH to cyberhire;

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

INSERT INTO cyberhire.skill (skill)
VALUES
('Python'),
('Java'),
('SQL'),
('JavaScript'),
('C++'),
('C#'),
('C')
;

-- Create the user_profile_skill 
CREATE TABLE IF NOT EXISTS cyberhire.user_profile_skill (
	user_profile_id int4 NOT NULL,
	skill_id int4 NOT NULL,
	CONSTRAINT user_profile_skill_user_profile_fk FOREIGN KEY (user_profile_id) REFERENCES cyberhire.user_profile (user_id),
	CONSTRAINT user_profile_skill_skill_fk2 FOREIGN KEY (skill_id) REFERENCES cyberhire.skill (id),
	CONSTRAINT user_profile_skill_unique UNIQUE (user_profile_id, skill_id)
);

-- Create for the job table
CREATE TABLE IF NOT EXISTS cyberhire."job" (
	id serial4 NOT NULL,
	user_profile_id int4 NOT NULL,
	title varchar(100) NOT NULL,
	description varchar(2000) NOT NULL,
	company_name varchar(100) NOT NULL,
	location varchar(100) NOT NULL,
	min_salary int4 NULL,
	max_salary int4 NULL,
	CONSTRAINT job_pkey PRIMARY KEY (id),
	CONSTRAINT job_user_profile_fk FOREIGN KEY (user_profile_id) REFERENCES cyberhire.user_profile (user_id)
);

-- Create for the job_skill table
CREATE TABLE IF NOT EXISTS cyberhire."job_skill" (
	job_id int4 NOT NULL,
	skill_id int4 NOT NULL,
	CONSTRAINT job_skill_pkey PRIMARY KEY (job_id, skill_id),
	CONSTRAINT job_skill_fk FOREIGN KEY (job_id) REFERENCES cyberhire."job" (id),
	CONSTRAINT job_skill_fk2 FOREIGN KEY (skill_id) REFERENCES cyberhire."skill" (id)
);

-- Create for the application_status table

CREATE TABLE IF NOT EXISTS cyberhire."application_status" (
	id serial4 PRIMARY KEY NOT NULL,
	status varchar(30) UNIQUE NOT NULL
);

INSERT INTO cyberhire."application_status" (status)
VALUES 
('SUBMITTED'),
('UNDER REVIEW'),
('UNDERGOING FURTHER SCREENING')
('REJECTED'),
('OFFER SENT')
;

-- Create for the user_profile_job table
CREATE TABLE IF NOT EXISTS cyberhire."user_profile_job" (
	user_profile_id int4 NOT NULL,
	job_id int4 NOT NULL,
	application_status_id int4 NOT NULL,
	application_submitted_date date NOT NULL,
	application_reviewed_date date NULL,
	application_further_screening_date date NULL,
	application_offer_sent_date date NULL,
	application_rejected_date date NULL,
	rejection_feedback varchar(2000) NULL,
	CONSTRAINT user_profile_job_pkey PRIMARY KEY (user_profile_id, job_id),
	CONSTRAINT user_profile_job_fk FOREIGN KEY (user_profile_id) REFERENCES cyberhire."user_profile" (user_id),
	CONSTRAINT user_profile_job_fk2 FOREIGN KEY (job_id) REFERENCES cyberhire."job" (id),
	CONSTRAINT user_profile_job_fk3 FOREIGN KEY (application_status_id) REFERENCES application_status (id)
);
