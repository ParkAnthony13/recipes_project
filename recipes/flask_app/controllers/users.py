from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if "user_id" in session:
        return redirect ('/dashboard')
    return render_template('home.html')


@app.route('/process',methods=['POST'])
def new_account():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user_id = User.insert(data)
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    data = {"email":request.form['login_email']}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password","perror")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Invalid Email/Password","perror")
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    recipes = Recipe.get_all()
    return render_template('dashboard.html',user=user,recipes=recipes)