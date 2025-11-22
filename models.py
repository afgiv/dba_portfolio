from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}

    user_id = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.Date, nullable = False)


class Students(db.Model):
    __tablename__ = "students"
    __table_args__ = {"schema": "app"}

    student_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    year_level = db.Column(db.Integer, nullable = False)

    user = db.relationship('Users', backref = 'students', uselist = False)
    courses = db.relationship('Courses', secondary = 'app.student_courses', backref='students')

class Faculty(db.Model):
    __tablename__ = "faculty"
    __table_args__ = {"schema": "app"}

    faculty_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    year_joined = db.Column(db.Integer, nullable = False)

    user = db.relationship('Users', backref = 'faculty', uselist = False)
    courses_assigned = db.relationship('Courses', secondary = 'app.courses_assigned', backref='faculty')

class Librarian(db.Model):
    __tablename__ = "librarian"
    __table_args__ = {"schema": "app"}

    lib_id = db.Column(db.String(50), db.ForeignKey('app.users.user_id'), primary_key = True)
    book_id = db.Column(db.Integer, nullable = False)
    book_title= db.Column(db.String(100), nullable = False)

    user = db.relationship('Users', backref = 'librarian', uselist = False)

class Courses(db.Model):
    __tablename__ = "courses"
    __table_args__ = {"schema": "app"}

    course_id = db.Column(db.Integer, primary_key = True)
    course_title = db.Column(db.String(120), nullable = False)
    course_units = db.Column(db.Integer, nullable = False)

class Student_Course(db.Model):
    __tablename__ = "student_courses"
    __table_args__ = {"schema": "app"}

    student_id = db.Column(db.String(50), db.ForeignKey('app.students.student_id'), primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey('app.courses.course_id'), primary_key = True)
    enrolled_at = db.Column(db.Date, nullable = False)

class Courses_Assigned(db.Model):
    __tablename__ = "courses_assigned"
    __table_args__ = {"schema": "app"}

    faculty_id = db.Column(db.String(50), db.ForeignKey('app.faculty.faculty_id'), primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey('app.courses.course_id'), primary_key = True)