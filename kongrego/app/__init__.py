from flask import Flask
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
import datetime
import requests
from  config import *

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)



app= Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')
#app.config["MONGO_URI"] = "mongodb://localhost:27017/inventory"
mongo = PyMongo(app)
from app import views
mongo.db.patch.insert_one({'patch': "Still_nothing_here"})
#app.json_encoder = JSONEncoder
