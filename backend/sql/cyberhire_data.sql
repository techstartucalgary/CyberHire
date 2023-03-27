--INSERT INTO cyberhire."user" (username, "password", email, is_recruiter)
--VALUES
--('testuser', 'testuser', 'testuser@gmail.com', false)
--;

INSERT INTO cyberhire."user" (user_id, first_name, last_name)
VALUES
(1, 'Ling', 'Lee')
;

--INSERT INTO cyberhire.skill (skill)
--VALUES
--('Python'),
--('Java'),
--('SQL'),
--('JavaScript'),
--('C++'),
--('C#'),
--('C')
--;

INSERT INTO cyberhire.user_profile_skill (user_profile_id, skill_id)
VALUES
(1, 1),
(1, 2),
(1, 3)
;

INSERT INTO cyberhire.job (user_profile_id, title, description, location, salary_range)
VALUES
(1, 'Python Developer', 'Test description', 'Calgary', '1')
;

INSERT INTO cyberhire.job_skill (job_id, skill_id)
VALUES
(1, 1),
(1, 2),
(1, 3)
;

--INSERT INTO cyberhire.application_status (status)
--VALUES
--('SUBMITTED'),
--('UNDER REVIEW'),
--('UNDERGOING FURTHER SCREENING'),
--('REJECTED'),
--('OFFER SENT')
--;

INSERT INTO cyberhire.user_profile_job (user_profile_id, job_id, application_status_id, application_submitted_date)
VALUES
(1, 1, 1, CURRENT_DATE)
;
