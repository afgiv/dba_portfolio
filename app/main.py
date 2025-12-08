# Import the necessary packages
from flask import Flask, request, render_template, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from models import db, Users, Students, Faculty, Librarian, Courses, Student_Course, Courses_Assigned, Books
from forms import NewUser, NewCourse, NewBook, NewEnrollment
from config import Config

# Create the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Connect to Bootstrap
Bootstrap5(app)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Initialize the Flask login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# Create the required role for each endpoint accessiblity
def admin_only(f):
    @wraps(f)
    def role_access(*args, **kwargs):
        if current_user.role != 'admin':
            return abort(403)
        return f(*args, **kwargs)
    return role_access

def student_only(f):
    @wraps(f)
    def role_access(*args, **kwargs):
        if current_user.role != 'student':
            return abort(403)
        return f(*args, **kwargs)
    return role_access

def faculty_only(f):
    @wraps(f)
    def role_access(*args, **kwargs):
        if current_user.role != 'faculty':
            return abort(403)
        return f(*args, **kwargs)
    return role_access

def librarian_only(f):
    @wraps(f)
    def role_access(*args, **kwargs):
        if current_user.role != 'librarian':
            return abort(403)
        return f(*args, **kwargs)
    return role_access


# Render the login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Get the credentials of the user from the form
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        # Check if the user is in the database
        user = Users.query.get(user_id)
        # Check if the credentials met with the one in the database
        if not user:
            flash("User ID does not exist, please contact the admin for further assistance.", "danger")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password Incorrect, please try again.", "danger")
            return redirect(url_for('login'))
        else:
            # If the login is successful, login the user depending on their role
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# Check the role of the user and render their page
@app.route('/dashboard', methods = ['GET'])
@login_required
def dashboard():
    role = current_user.role
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'faculty':
        return redirect(url_for('faculty_dashboard'))
    elif role == 'librarian':
        return redirect(url_for('librarian_dashboard'))
    elif role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        flash("Role not recognized", "danger")
        return redirect(url_for('login'))

# --------------------------------- STUDENTS --------------------------------- #
# Render the list of courses the user (student) enrolled to
@app.route("/student_dashboard/my_courses" , methods = ['GET'])
@login_required
@student_only
def student_dashboard():
    student_id = current_user.user_id
    student = Students.query.get(student_id)
    my_courses = [{
        "course_title": my.courses.course_title,
        "course_units": my.courses.course_units,
        "enrolled_at": my.enrolled_at
    } for my in student.enrolled ]

    return render_template('index.html', page="student", dashboard="my_courses", courses=my_courses)

# Render the list of courses available for the user (student) to see
@app.route("/student_dashboard/courses", methods = ['GET'])
@login_required
@student_only
def list_of_courses():
    courses = Courses.query.all()
    return render_template('index.html', page="student", dashboard="list", courses=courses)

# --------------------------------- STUDENTS --------------------------------- #

# --------------------------------- FACULTY --------------------------------- #

# Render the list of courses the user (faculty) is assigned to
@app.route("/faculty_dashboard/my_courses" , methods = ['GET'])
@login_required
@faculty_only
def faculty_dashboard():
    faculty_id = current_user.user_id
    faculty = Faculty.query.get(faculty_id)
    my_courses = [{
        "course_title": my.courses.course_title,
        "course_units": my.courses.course_units
    } for my in faculty.courses_assigned ]
    return render_template('index.html', page="faculty", dashboard="my_courses", courses=my_courses)

# Render the list of students of the user (faculty)
@app.route("/faculty_dashboard/my_students", methods = ['GET'])
@login_required
@faculty_only
def list_of_students():
    faculty_id = current_user.user_id
    faculty = Faculty.query.get(faculty_id)
    my_students = [{
        "course_title": my.courses.course_title,
        "course_units": my.courses.course_units,
        "my_students": [{
            "first_name": student.first_name,
            "last_name": student.last_name
        } for student in my.courses.students]
    } for my in faculty.courses_assigned ]
    return render_template('index.html', page="faculty", dashboard="students", students=my_students,)

# --------------------------------- FACULTY --------------------------------- #


# --------------------------------- LIBRARIAN --------------------------------- #
# Render the list of books of the user (librarian) to manage
@app.route("/librarian_dashboard/books" , methods = ['GET'])
@login_required
@librarian_only
def librarian_dashboard():
    books = db.session.query(Librarian).all()
    return render_template('index.html', page="librarian", dashboard="books", books=books)

# Render the form for registering new book
@app.route("/librarian_dashboard/add_book", methods = ['GET', 'POST'])
@login_required
@librarian_only
def add_book():
    form = NewBook()
    if form.validate_on_submit():
        new_book = Books(
            lib_id = current_user.user_id,
            book_id = form.book_id.data,
            book_title = form.book_title.data,
            book_author = form.book_author.data
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('librarian_dashboard'))
    return render_template('index.html', page='librarian', dashboard='new_book', form=form)


# --------------------------------- LIBRARIAN --------------------------------- #


# --------------------------------- ADMIN --------------------------------- #
# Render the admin page for adding new user
@app.route("/admin/new_user" , methods = ['GET', 'POST'])
@login_required
@admin_only
def admin_dashboard():
    form = NewUser()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=16)
        role = form.role.data
        user = form.user_id.data
        true_user = Users.query.get(user)
        if true_user:
            flash("User already exists!", "danger")
        else:
            new_user = Users(
                user_id = user,
                password = hashed_password,
                role = form.role.data
            )
            db.session.add(new_user)
            # add the details of the user depending on their role
            if role == 'student':
                new_student = Students(
                    student_id = user,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    birthdate = form.birthdate.data,
                    year_level = form.year.data
                )
                db.session.add(new_student)
            elif role == 'faculty':
                new_faculty = Faculty(
                    faculty_id = user,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    birthdate = form.birthdate.data,
                    year_joined = form.year.data
                )
                db.session.add(new_faculty)
            elif role == 'librarian':
                new_librarian = Librarian(
                    lib_id = user,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    birthdate = form.birthdate.data,
                    year_joined = form.year.data
                )
                db.session.add(new_librarian)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
    return render_template('index.html', page="admin", form=form, dashboard="new_user")

# Render the admin page for adding new course
@app.route("/admin/new_course" , methods = ['GET', 'POST'])
@login_required
@admin_only
def new_course():
    form = NewCourse()
    if form.validate_on_submit():
        new_course = Courses(
            course_id = form.course_id.data,
            course_title = form.course_title.data,
            course_units = form.course_units.data
        )
        db.session.add(new_course)
        new_assignment = Courses_Assigned(
            faculty_id = form.assigned_to.data,
            course_id = form.course_id.data
        )
        db.session.add(new_assignment)
        db.session.commit()
        return redirect(url_for('new_course'))
    return render_template('index.html', page="admin", form=form, dashboard="new_course")

# Render the admin page for adding new enrollment
@app.route("/admin/new_enrollment", methods = ['GET', 'POST'])
@login_required
@admin_only
def new_enrollment():
    form = NewEnrollment()
    if form.validate_on_submit():
        new_enrollment = Student_Course(
            student_id = form.student_id.data,
            course_id = form.course_id.data,
            enrolled_at = form.enrolled_at.data
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return redirect(url_for('new_enrollment'))
    return render_template('index.html', page="admin", form=form, dashboard="new_enrollment")

# --------------------------------- ADMIN --------------------------------- #

# Logout the user and return to the login page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))




# Start the flask app
if __name__ == "__main__":
    app.run(debug=True)
