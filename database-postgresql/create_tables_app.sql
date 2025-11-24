/* Create the tables for the app */



-- Create the users table
CREATE TABLE IF NOT EXISTS app.users (
	user_id VARCHAR(50) PRIMARY KEY,
	password VARCHAR(20) NOT NULL,
	role VARCHAR(20) NOT NULL,
	created_at DATE DEFAULT CURRENT_DATE NOT NULL
);

-- Create the students table
CREATE TABLE IF NOT EXISTS app.students (
	student_id VARCHAR(50) PRIMARY KEY,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	birthdate DATE NOT NULL,
	year_level INTEGER NOT NULL,
	CONSTRAINT fk_student_id FOREIGN KEY (student_id) REFERENCES app.users (user_id)
);

-- Create the faculty table
CREATE TABLE IF NOT EXISTS app.faculty (
	faculty_id VARCHAR(50) PRIMARY KEY,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	birthdate DATE NOT NULL,
	year_joined INTEGER NOT NULL,
	CONSTRAINT fk_faculty_id FOREIGN KEY (faculty_id) REFERENCES app.users (user_id)
);

-- Create the librarian table
CREATE TABLE IF NOT EXISTS app.librarian (
	lib_id VARCHAR(50) PRIMARY KEY,
	book_id INTEGER NOT NULL,
	book_title VARCHAR(100) NOT NULL,
	book_author VARCHAR(100) NOT NULL,
	CONSTRAINT fk_lib_id FOREIGN KEY (lib_id) REFERENCES app.users (user_id)
);

-- Create the courses table
CREATE TABLE IF NOT EXISTS app.courses (
	course_id SERIAL PRIMARY KEY,
	course_title VARCHAR(120) NOT NULL,
	course_units INTEGER NOT NULL
);

-- Create the junction table student_courses
CREATE TABLE IF NOT EXISTS app.student_courses (
	course_id INTEGER NOT NULL,
	student_id VARCHAR(50) NOT NULL,
	enrolled_at DATE NOT NULL,
	CONSTRAINT pk_stc PRIMARY KEY (course_id, student_id),
	CONSTRAINT fk_stc_course FOREIGN KEY (course_id) REFERENCES app.courses (course_id),
	CONSTRAINT fk_stc_student FOREIGN KEY (student_id) REFERENCES app.students (student_id)
);

-- Create the junction table courses_assigned
CREATE TABLE IF NOT EXISTS app.courses_assigned (
	course_id INTEGER NOT NULL,
	faculty_id VARCHAR(50) NOT NULL,
	CONSTRAINT pk_ca PRIMARY KEY (course_id, faculty_id),
	CONSTRAINT fk_ca_course FOREIGN KEY (course_id) REFERENCES app.courses (course_id),
	CONSTRAINT fk_ca_student FOREIGN KEY (faculty_id) REFERENCES app.faculty (faculty_id)
);