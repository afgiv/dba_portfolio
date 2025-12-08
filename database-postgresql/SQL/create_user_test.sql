-- Create the sample test for each user type

INSERT INTO app.users (user_id, password, role)
VALUES ('S-20251010', 'test', 'student');

INSERT INTO app.students (student_id, first_name, last_name, birthdate, year_level)
VALUES('S-20251010', 'John', 'Smith', '09-27-2000', '1');

INSERT INTO app.users (user_id, password, role)
VALUES ('F-20251010', 'test', 'faculty');

INSERT INTO app.faculty (faculty_id, first_name, last_name, birthdate, year_joined)
VALUES ('F-20251010', 'Alice', 'Wonders', '01-20-1990', '2023');

INSERT INTO app.users (user_id, password, role)
VALUES ('L-20251010', 'test', 'librarian');

INSERT INTO app.librarian (lib_id, book_id, book_title, book_author)
VALUES ('L-20251010', '101', 'Intro to Database', 'James Webb	');

INSERT INTO app.users (user_id, password, role)
VALUES ('admin', 'admin', 'admin');

-- Create the sample test for student course
INSERT INTO app.courses (course_id, course_title, course_units)
VALUES ('101', 'Intro to Database', '3');

INSERT INTO app.student_courses (course_id, student_id, enrolled_at)
VALUES ('101', 'S-20251010', '11-21-2025');

-- Create the sample test for faculty course
INSERT INTO app.courses_assigned (course_id, faculty_id)
VALUES ('101', 'F-20251010');