# Import the necessary packages
from flask import Flask, request, render_template, flash, url_for, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Users, Students, Faculty, Librarian, Courses, Student_Course, Courses_Assigned
from config import Config

# Create the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Render the login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Get the credentials of the user from the form
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        # Check if the user is in the database
        result = db.session.execute(db.select(Users).where(Users.user_id == user_id))
        user = result.scalar()
        # Check if the credentials met with the one in the database
        if not user:
            flash("User ID does not exist, please contact the admin for further assistance.", "danger")
            return redirect(url_for('login'))
        elif user.password != password:
            flash("Password Incorrect, please try again.", "danger")
            return redirect(url_for('login'))
        else:
            # If the login is successful, login the user depending on their role
            login_user(user)
            session['role'] = user.role
            print('eyy')
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# Check the role of the user and render their page
@app.route('/dashboard', methods = ['GET'])
@login_required
def dashboard():
    role = current_user.role
    print(current_user.user_id)
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


@app.route("/student_dashboard/" , methods = ['GET'])
@login_required
def student_dashboard():
    return render_template('index.html')





# Start the flask app
if __name__ == "__main__":
    app.run(debug=True)
