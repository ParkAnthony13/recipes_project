from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.time = data['time']
        self.instructions = data['instructions']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        if len(results)>0:
            for recipe in results:
                data = {
                    "id":recipe['id'],
                    "name":recipe['name'],
                    "time":recipe['time'],
                    "instructions":recipe['instructions'],
                    "description":recipe['description'],
                    "created_at":recipe['created_at'],
                    "updated_at":recipe['updated_at'],
                    "user":user.User.get_by_id({"id":recipe['user_id']})
                }
                recipes.append(cls(data))
            return recipes
    

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        one_recipe = {
            "id":results[0]['id'],
            "name":results[0]['name'],
            "time":results[0]['time'],
            "instructions":results[0]['instructions'],
            "description":results[0]['description'],
            "created_at":results[0]['created_at'],
            "updated_at":results[0]['updated_at'],
            "user":user.User.get_by_id({"id":results[0]['user_id']})
        }
        return cls(one_recipe)



    @classmethod
    def insert_recipe(cls,data):
        query = "INSERT INTO recipes (name,time,instructions,description,created_at, updated_at,user_id) VALUES(%(name)s,%(time)s,%(instructions)s,%(description)s,%(created_at)s, NOW(),%(user_id)s);"
        return connectToMySQL('recipes_schema').query_db(query,data)


    @classmethod
    def update_recipe(cls,data):
        print(data)
        query = "UPDATE recipes SET name=%(name)s,time=%(time)s,instructions=%(instructions)s,description=%(description)s,created_at=%(created_at)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM emails WHERE id=%(id)s"
        return connectToMySQL('recipes_schema').query_db(query,data)

