import os
from flask import Flask
from flask_pymongo import PyMongo

#Create an Instance of Flask
app = Flask(__name__, instance_relative_config=True)

#Include config from config.py
app.config.from_object('config')
#app.config.from_pyfile('config.py')
app.secret_key = '\xa6\x8f\xb8d\x00\xdaH\xd2i\x96\xc9v0$]:\xae\xdb\xd3\xd9k\xa2\xe5\x9a'

mongo = None #PyMongo(app)

from app import views
