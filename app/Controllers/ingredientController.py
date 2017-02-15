from flask import Flask, jsonify, render_template, Blueprint, request
from bson.json_util import dumps, loads
from app.db.database import Ingredient
import bson
import urllib.request
import json

app = Flask(__name__)

ingredientController = Blueprint('ingredientController', __name__)

class IngredientController(object):
    @ingredientController.route('s/', methods=['GET'])
    def index():
        ingredient = Ingredient.find() #Get all documents
        ingredientCount = Ingredient.count() #Get all documents
        return dumps(ingredient) #dumps all to json

    @ingredientController.route('/<string:id>', methods=['GET'])
    def show(id):
        ingredient = Ingredient.find_one({"_id": bson.ObjectId(oid=str(id))}) #get id ObjectId and the informartions sent
        return dumps(ingredient)#dumps all to json

    @ingredientController.route('/update/<string:id>', methods=['PUT', 'GET'])
    def update(id):
        data = request.json #get id ObjectId and the informartions sent

        return 'Updated'

    @ingredientController.route('/create', methods=['POST', 'GET'])
    def create():

        return 'Done'

    @ingredientController.route('/delete/<string:id>', methods=['DELETE','GET'])
    def delete(id):
        delete = Ingredient.delete_one({"_id": bson.ObjectId(oid=str(id))}) #Take the ObjectId from recepie and delete that documnet
        delete_count = delete.deleted_count
        return 'Delete ' + dumps(delete_count) + ' document'
