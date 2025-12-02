from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


# Create the form for registering new User
class NewUser(FlaskForm):
    user_id = StringField(label="User ID", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    role = SelectField(label="Role", choices=[('student', 'Student'), 
                                              ('faculty', 'Faculty'), ('librarian', 'Librarian')], validators=[DataRequired()])
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    birthdate = DateField(label="Birthdate", validators=[DataRequired()])
    year = IntegerField(label="Year Level/Year Joined")
    submit = SubmitField(label="Add user")

# Create the form for registering new course
class NewCourse(FlaskForm):
    course_id = IntegerField(label="Course ID", validators=[DataRequired()])
    course_title = StringField(label="Title", validators=[DataRequired()])
    course_units = IntegerField(label="Units", validators=[DataRequired()])
    assigned_to = StringField(label="Assigned to", validators=[DataRequired()])
    submit = SubmitField(label="Add course")


class NewBook(FlaskForm):
    book_id = IntegerField(label="Book ID", validators=[DataRequired()])
    book_title = StringField(label="Title", validators=[DataRequired()])
    book_author = StringField(label="Author", validators=[DataRequired()])
    submit = SubmitField(label="Add book")

class NewEnrollment(FlaskForm):
    student_id = StringField(label="Student ID", validators=[DataRequired()])
    course_id = IntegerField(label="Course ID", validators=[DataRequired()])
    enrolled_at = DateField(label="Enrolled at", validators=[DataRequired()])
    submit = SubmitField(label="Enroll")
