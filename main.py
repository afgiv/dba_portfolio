# Import the necessary packages
from flask import Flask, request, render_template, flash, url_for, redirect
from sqlalchemy import Integer, String, Date
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

# Create the Flask app
app = Flask(__name__)