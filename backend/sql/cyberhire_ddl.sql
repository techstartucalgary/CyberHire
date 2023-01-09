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

CREATE TABLE IF NOT EXISTS cyberhire."skill" (
	id serial4 NOT NULL,
	skill varchar(30) NOT NULL UNIQUE,
	CONSTRAINT skill_pkey PRIMARY KEY (id),
	CONSTRAINT skill_skill_unique UNIQUE (skill)
);

CREATE TABLE IF NOT EXISTS cyberhire.user_skill (
	user_id int4 NOT NULL,
	skill_id int4 NOT NULL,
	CONSTRAINT user_skill_user_fk FOREIGN KEY (user_id) REFERENCES cyberhire.user (id),
	CONSTRAINT user_skill_skill_fk2 FOREIGN KEY (skill_id) REFERENCES cyberhire.skill (id)
);