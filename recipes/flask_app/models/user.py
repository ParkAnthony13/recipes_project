from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe
import re
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#

class User:
    def __init__( self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL("recipes_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id=%(id)s;"
        results = connectToMySQL("recipes_schema").query_db(query,data)

        user = cls(results[0])
        if results[0]['recipes.id'] != None:
            for row in results:
                row_data = {
                    'id': row['recipes.id'],
                    'name': row['name'],
                    'time':row['time'],
                    'instructions':row['instructions'],
                    'description':row['description'],
                    'created_at':row['recipes.created_at'],
                    'updated_at':row['recipes.updated_at'],
                    'user':user
                }
                user.recipes.append(Recipe(row_data))
        return user


    @classmethod
    def insert(cls,data):
        query="INSERT INTO users(first_name,last_name,email,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL("recipes_schema").query_db(query,data)



    @staticmethod  # make sure no duplicate email # has email structure
    def validate_user(data):
        is_valid = True # the keys must match the request.form keys or NAME in the HTML
        if len(data['first_name']) < 2:
            flash("Name must be at least 3 characters.",'name')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("last must be at least 3 characters.","name")
            is_valid = False
        if not data['first_name'].isalpha():
            flash("May not contain non alphabetical characters","name")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!",'emailError')
            is_valid = False
        elif User.duplicates(data['email']):
            flash("Invalid email address!",'emailError')
            is_valid = False
        if len(data['password']) < 3:
            flash("password must be at least 3 characters.","password")
            is_valid = False
        if data['password'] != data['confirm']:
            flash("Passwords must Match","confirm")
        flash(f"You have successfully logged in with : {data['email']}","success")
        return is_valid


    @staticmethod  # make sure no duplicate email # has email structure
    def validate_create(data):
        is_valid = True # the keys must match the request.form keys or NAME in the HTML
        if len(data['name']) < 2:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if 'time' not in data:
            flash("Must choose option.")
            is_valid = False
        if 'instructions' not in data:
            flash("Must include instructions")
            is_valid = False
        if 'description' not in data:
            flash("Must include Description")
            is_valid = False
        if 'created_at' not in data:
            flash("Please choose a date")
            is_valid = False
        return is_valid


    @staticmethod
    def duplicates(data):
        query = "SELECT * FROM emails WHERE email=%(email)s;"
        result = connectToMySQL('recipes_schema').query_db(query,data)
        duplicate = False
        if result:
            duplicate = True
        return duplicate