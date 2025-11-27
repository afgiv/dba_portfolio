from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}

    user_id = db.Column(db.String(50), primary_key = True, index = True)
    password = db.Column(db.Text, nullable = False)
    role = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.Date, server_default = func.current_date(), nullable = False)

    def get_id(self):
        return self.user_id


class Students(db.Model):
    __tablename__ = "students"
    __table_args__ = {"schema": "app"}

    student_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True, index = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    year_level = db.Column(db.Integer, nullable = False)

    user = db.relationship('Users', backref = 'students', uselist = False)
    courses = db.relationship('Courses', secondary = 'app.student_courses', backref='students')
    enrolled = db.relationship('Student_Course', backref='students')

class Faculty(db.Model):
    __tablename__ = "faculty"
    __table_args__ = {"schema": "app"}

    faculty_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True, index = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    year_joined = db.Column(db.Integer, nullable = False)

    user = db.relationship('Users', backref = 'faculty', uselist = False)
    courses_assigned = db.relationship('Courses_Assigned', backref='faculty')

class Librarian(db.Model):
    __tablename__ = "librarian"
    __table_args__ = {"schema": "app"}

    lib_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True, index = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    year_joined = db.Column(db.Integer, nullable = False)

    user = db.relationship('Users', backref = 'librarian', uselist = False)
    books_registered = db.relationship('Books', backref = 'librarian')

class Books(db.Model):
    __tablename__ = "books"
    __table_args__ = {"schema": "app"}

    lib_id = db.Column(db.String(50), db.ForeignKey('app.librarian.lib_id'))
    book_id = db.Column(db.Integer, nullable = False, primary_key = True, index = True)
    book_title= db.Column(db.String(100), nullable = False)
    book_author = db.Column(db.String(100), nullable = False)

class Courses(db.Model):
    __tablename__ = "courses"
    __table_args__ = {"schema": "app"}

    course_id = db.Column(db.Integer, primary_key = True, index = True)
    course_title = db.Column(db.String(120), nullable = False)
    course_units = db.Column(db.Integer, nullable = False)

    enrolled = db.relationship('Student_Course', backref='courses')
    assigned = db.relationship('Courses_Assigned', backref='courses')

class Student_Course(db.Model):
    __tablename__ = "student_courses"
    __table_args__ = {"schema": "app"}

    student_id = db.Column(db.String(50), db.ForeignKey('app.students.student_id'), primary_key = True, index = True)
    course_id = db.Column(db.Integer, db.ForeignKey('app.courses.course_id'), primary_key = True, index = True)
    enrolled_at = db.Column(db.Date, nullable = False)

class Courses_Assigned(db.Model):
    __tablename__ = "courses_assigned"
    __table_args__ = {"schema": "app"}

    faculty_id = db.Column(db.String(50), db.ForeignKey('app.faculty.faculty_id'), primary_key = True, index = True)
    course_id = db.Column(db.Integer, db.ForeignKey('app.courses.course_id'), primary_key = True, index = True)