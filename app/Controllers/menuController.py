from flask import Flask, jsonify, render_template, Blueprint, request
from bson.json_util import dumps
from app.db.database import Menu
import bson
import datetime

app = Flask(__name__)

menuController = Blueprint('menuController', __name__)

class MenuController(object):
    @menuController.route('s/', methods=['GET'])
    def index():
        menuoutput = Menu.find() #Get all documents
        return  dumps(menuoutput)

    @menuController.route('/<string:id>', methods=['GET'])
    def show(id):
        oneMenu = Menu.find_one({"_id": bson.ObjectId(oid=str(id))})
        return dumps(oneMenu)

    @menuController.route('/create', methods=['POST', 'GET'])
    def create():
        data = request.json
        MenuData = {
        'Title':  data['Title'],
        'Description': data['Description'],
        'Recipes': data['Recipes'],
        'Tags': data['Tags'],
        'Access':  data['Access'],
        'Owner': data['Owner'],
        'Public': data['Public'],
        "CreateDate": datetime.datetime.now() # set the date
        }
        Menu.insert_one(MenuData)
        return 'Menu added'

    @menuController.route('/update/<string:id>', methods=['PUT', 'GET'])
    def update(id):
        data = request.json #get id ObjectId and the informartions sent
        Menu.update_many(
            {"_id": bson.ObjectId(oid=str(id))}, #get the bson ObjectId as a string
            {
                "$set": { #update fields
                    'Title':  data['Title'],
                    'Description': data['Description'],
                    'Recipes': data['Recipes'],
                    'Tags': data['Tags'],
                    'Access':  data['Access'],
                    'Owner': data['Owner'],
                    'Public': data['Public']
                },
                "$currentDate": {"lastModified": True} # set the update date
            }
        )
        return 'Menu added updated'

    @menuController.route('/delete/<string:id>', methods=['DELETE','GET'])
    def delete(id):
        delete = Menu.delete_one({"_id": bson.ObjectId(oid=str(id))})#Take the ObjectId from recepie and delete that documnet
        delete_count = delete.deleted_count
        return 'Delete ' + dumps(delete_count) + ' document'
