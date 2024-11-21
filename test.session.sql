INSERT INTO user (user_email, user_first, user_last, user_password) VALUES ('bartholomew@aol.com', 'Bartholomew', 'Cornelius', 'password')
INSERT INTO user (user_email, user_first, user_last, user_password) VALUES ('drewbrees@gmail.com', 'Drew', 'Brees', 'password1')
INSERT INTO user (user_email, user_first, user_last, user_password) VALUES ('toothless@yahoo.com', 'Toothless', 'Dragon', 'hiccup')

INSERT INTO role (role_name, description) VALUES ('Student', 'Someone who attends classes and pays tuition');
INSERT INTO role (role_name, description) VALUES ('Admin', 'Administrator with full access to all features.');
INSERT INTO role (role_name, description) VALUES ('Tutor', 'Responsible for guiding and assisting students in their learning process.');
INSERT INTO role (role_name, description) VALUES ('Teaching Assistant', 'Helps teach newer students');
INSERT INTO role (role_name, description) VALUES ('Teacher', 'Responsible for planning, delivering lessons, and assessing student progress.');
INSERT INTO role (role_name, description) VALUES ('Staff Member', 'Support and manage institutional operations and administrative tasks.');

INSERT INTO userrole VALUES (1, 3);
INSERT INTO userrole VALUES (1, 1);
INSERT INTO userrole VALUES (2, 3);
INSERT INTO userrole VALUES (2, 2);
INSERT INTO userrole VALUES (3, 1);
INSERT INTO userrole VALUES (3, 3);
INSERT INTO userrole VALUES (3, 5);