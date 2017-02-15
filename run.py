from flask import Flask, render_template, Blueprint
from app.Controllers.recipeController import recipeController
from app.Controllers.userController import userController
from app.Controllers.ingredientController import ingredientController
from app.Controllers.listController import listController
from app.Controllers.menuController import menuController
from app.Controllers.apiController import apiController
from flask.ext.cors import CORS
app = Flask(__name__)

################ USER CORS START ################
cors = CORS(app, resources={r"/users/*": {"origins": "*"}})
################ USER CORS STOP ################

################ RECIPE CORS START ################
cors = CORS(app, resources={r"/recipes/": {"origins": "*"}})
cors = CORS(app, resources={r"/recipe/*": {"origins": "*"}})
################ RECIPE CORS STOP ################

################ INGREDIENT CORS START ################
cors = CORS(app, resources={r"/ingredient/*": {"origins": "*"}})
################ INGREDIENT CORS STOP ################

################ MENU CORS START ################
cors = CORS(app, resources={r"/menu*": {"origins": "*"}})
################ MENU CORS STOP ################

################ MENU CORS START ################
cors = CORS(app, resources={r"/api*": {"origins": "*"}})
################ MENU CORS STOP ################

app.register_blueprint(recipeController, url_prefix='/recipe')
app.register_blueprint(userController, url_prefix='/user')
app.register_blueprint(ingredientController, url_prefix='/ingredient')
app.register_blueprint(listController, url_prefix='/list')
app.register_blueprint(menuController, url_prefix='/menu')
app.register_blueprint(apiController, url_prefix='/api')

if __name__ == "__main__":
    app.debug = True
    app.run(host = '188.166.147.218', threaded=True)
