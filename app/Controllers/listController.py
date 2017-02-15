from flask import Flask, jsonify, render_template, Blueprint, request
from bson.json_util import dumps
from app.db.database import List
import bson

app = Flask(__name__)

listController = Blueprint('listController', __name__)

class ListController(object):

    @listController.route('s/', methods=['GET'])
    def index():
        list_one = List.find() #Get all documents
        return dumps(list_one) #dumps all to json

    @listController.route('/<id>', methods=['GET'])
    def show(id):
        list_id = List.find_one({"_id": bson.ObjectId(oid=str(id))})
        return dumps(list_id)#dumps all to json


    # get and add list with both hashes and validation
    @listController.route('/create', methods=['POST'])
    def create():
        data = request.json
        Title = data['Title']
        Ingredient = data['Ingredient']
        lists = {
        "Title" : title, #max characters in validation
        "Ingredient" : ingredient  #needs to find the right ingredients
        }
        List.insert_one(lists)
        return dumps(lists)
