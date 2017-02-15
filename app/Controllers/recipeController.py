from flask import Flask, jsonify, render_template, Blueprint, request
from bson.json_util import dumps
from app.db.database import Recipe
import bson
import datetime

app = Flask(__name__)

recipeController = Blueprint('recipeController', __name__)


class RecipeController(object):
    @recipeController.route('s/', methods=['GET'])
    def index():
        recipe = Recipe.find() #Get all documents
        return dumps(recipe) #dumps all to json

    @recipeController.route('/<string:id>', methods=['GET'])
    def show(id):
        recipe = Recipe.find_one({"_id": bson.ObjectId(oid=str(id))})
        return dumps(recipe)#dumps all to json

    @recipeController.route('/update/<string:id>', methods=['PUT', 'GET'])
    def update(id):
        data = request.json #get id ObjectId and the informartions sent
        Recipe.update_many(
            {"_id": bson.ObjectId(oid=str(id))}, #get the bson ObjectId as a string
            {
                "$set": { #update fields
                    'Title':  data['Title'],
                    'Description': data['Description'],
                    'Portions': data['Portions'],
                    'Step': data['Step'],
                    'Ingredients': data['Ingredients'],
                    'Categories': data['Categories'],
                    'Tags': data['Tags'],
                    'Reference':  data['Reference']
                },
                "$currentDate": {"lastModified": True} # set the update date
            }
        )
        return dumps(id)

    @recipeController.route('/create', methods=['POST', 'GET'])
    def create():
        data = request.json
        # Validate the informartions about recipe. No blanks is OK
        if data['Title'] and data['Description'] and data['Portions'] and data['Step'] and data['Ingredients'] and data['Categories'] and data['Tags'] != "":
            recipeData = {
            'Title':  data['Title'],
            'Description': data['Description'],
            'Portions': data['Portions'],
            'Step': data['Step'],
            'Ingredients': data['Ingredients'],
            'Categories': data['Categories'],
            'Tags': data['Tags'],
            'Rating':  data['Rating'],
            'Reference':  data['Reference'],
            "CreateDate": datetime.datetime.now() # set the date
            }
            Recipe.insert_one(recipeData)
            return 'Done'
        else:
            return 'Missing value'

    @recipeController.route('/delete/<string:id>', methods=['DELETE','GET'])
    def delete(id):
        delete = Recipe.delete_one({"_id": bson.ObjectId(oid=str(id))})#Take the ObjectId from recepie and delete that documnet
        delete_count = delete.deleted_count
        return 'Delete ' + dumps(delete_count) + ' document'
