from flask import Blueprint, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from __main__ import db
from models.user_model import User
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route("/")
def hello():
    return "Hello, auth!"

# test route for checking workable database api
@auth.route("/name")
def name():
    print(User.query.select_from().first().name)
    return "OK"

@auth.route("/signup", methods = ['POST'])
def signup():
    # email = request.form.get('email')
    # name = request.form.get('name')
    # password = request.form.get('password')

    email = request.json['email']
    name = request.json['name']
    password = request.json['password']

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return "Учётная запись уже существует" #redirect(url_for('auth.signin'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return "Учётная запись создана" #redirect(url_for('auth/signin'))

@auth.route("/signin", methods = ['POST'])
def signin():
    # email = request.form.get('email')
    # password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    email = request.json['email']
    password = request.json['password']
    remember = True if request.json['remember'] else False
    print(remember)

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return "Не удалось выполнить вход" #redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return f"Вход выполнен. Здравствуйте, {current_user.name}!" #redirect(url_for('main.profile'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "Выход выполнен"
