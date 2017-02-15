from flask import Flask, jsonify, render_template, Blueprint, request
from bson.json_util import dumps, loads
from app.db.database import db
import bson
import urllib.request
import json
import time
import requests
app = Flask(__name__)

apiController = Blueprint('apiController', __name__)

class ApiController(object):
    #getmatapi copy data from Matapi.se till collection ingredients
    @apiController.route('/getmatapi', methods=['POST','GET'])
    def getmatapi():

        # GET INFO About the api
        request = urllib.request.Request("http://www.matapi.se/foodstuff/")
        response = urllib.request.urlopen(request)
        encoding = response.info().get_content_charset('utf8')
        alldata = json.loads(response.read().decode(encoding))
        data = alldata

        i=1 #counter
        for number, value in enumerate(data): #loop all data form data dict
            response = requests.get('http://www.matapi.se/foodstuff/'+str(i)) #check the url
            if response.status_code == 404: # if error 404 not found, only count
                i = i + 1
            else: # if url excist push to DB
                request = urllib.request.Request("http://www.matapi.se/foodstuff/"+str(i))
                response = urllib.request.urlopen(request)
                encoding = response.info().get_content_charset('utf8')
                data = json.loads(response.read().decode(encoding))
                db['ingredients'].insert_one(data) #push to db Ingredients
                i = i + 1
                time.sleep(2) # pause every time 2sec
        else:
            return 'All Done' #Show message when done
