from flask_app import app
from flask import render_template, request, session, redirect
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/create_page')
def new_recipe_page():
    if "user_id" not in session:
        return redirect('/')
    return render_template('recipe_new.html')


@app.route('/create/process',methods=['POST'])
def insert_recipe():
    if not User.validate_create(request.form):
        return redirect('/create_page')
    data = {
        "name":request.form['name'],
        "time":request.form['time'],
        "instructions":request.form['instructions'],
        "description":request.form['description'],
        "created_at":request.form['created_at'],
        "user_id":session['user_id']
    }
    Recipe.insert_recipe(data)
    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def update_recipe_page(id):
    if "user_id" not in session:
        return redirect('/')
    recipe = Recipe.get_one_by_id({"id":id})
    return render_template('recipe_edit.html',recipe=recipe)


@app.route('/update/process',methods=['POST'])
def update_recipe():

    if not User.validate_create(request.form):
        return redirect(f"/edit/{request.form['id']}")
    data = {
        "name":request.form['name'],
        "time":request.form['time'],
        "instructions":request.form['instructions'],
        "description":request.form['description'],
        "created_at":request.form['created_at'],
        "id":request.form['id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>')
def view_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    recipes = Recipe.get_one_by_id({"id":id})
    return render_template(f'recipe_page.html',user=user,recipes=recipes)