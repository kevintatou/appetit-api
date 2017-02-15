from flask import Flask, Blueprint, request, abort, json, jsonify
from bson.json_util import dumps, loads
from app.db.database import User
from flask.ext.bcrypt import Bcrypt
from bson.objectid import ObjectId
from itsdangerous import (TimedJSONWebSignatureSerializer
  as Serializer, BadSignature, SignatureExpired)
import uuid
app = Flask(__name__)
bcrypt = Bcrypt(app)
userController = Blueprint('userController', __name__)

class UserController(object):
    @userController.route('s/', methods=['GET'])
    def index():
        users = User.find()
        return dumps(users)

    # Register form with both hashes and validation
    @userController.route('/create', methods=['POST'])
    def create():
        data = request.json
        email = len(data['Email'])
        password = len(data['Password'])
        if(password < 4 or password > 10) and (email < 11 or email > 20):
            return "Fel"
        else:
            salt = uuid.uuid4().bytes
            hash_password = bcrypt.generate_password_hash(data['Password'])
            pw = hash_password + salt
            users = {
            "firstName": "",
            "lastName": "",
            "birthDay": "",
            "country": "",
            "city": "",
            "adress": "",
            "zipCode": "",
            "nickname": "",
            "token": "",
            "Email": data['Email'],
            "Password": pw
            }
            User.insert_one(users)
        return dumps(users)

    #Route for getting one user by its ObjectID
    @userController.route('/<id>', methods=['GET'])
    def show(id):
        user = User.find_one({'_id': ObjectId(id)})
        return dumps(user)

    @userController.route('/update', methods=['PUT'])
    def update():
        user = User.find_one({'_id': ObjectId(id)})
        return dumps(user)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'_id' : self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # if the token is valid, but is expired
        except BadSignature:
            return None # the token is invalid
        user = User.find_one({'_id'})
        return user
