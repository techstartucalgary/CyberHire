INSERT INTO cyberhire."user" (username, "password", email, is_recruiter)
VALUES
('testuser', 'testuser', 'testuser@gmail.com', false)
;

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

INSERT INTO cyberhire.user_profile (user_id, first_name, last_name)
VALUES
(1, 'Ling', 'Lee')
;

INSERT INTO cyberhire.user_profile_skill (user_profile_id, skill_id)
VALUES
(1, 1),
(1, 2),
(1, 3)
;