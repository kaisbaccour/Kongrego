import uuid
from app import app
from flask import jsonify, request
from flask_pymongo import PyMongo
import json
import os
from bson.json_util import dumps
import pymongo, requests
import datetime
from config import *
import app.utils

mongo = PyMongo(app)
with app.app_context():
    mongo.db.inventory.create_index([("vmname", pymongo.ASCENDING)], unique=False)
es = Elasticsearch(hosts=ES_HOST+":"+ES_PORT, serializer=JSONSerializerPython2())

@app.route('/api/<string:env>/<string:microservice>', methods=['GET'])
def inventory_microservice(microservice,env):

    servers_running_ms=[]
    if request.method == 'GET':
        data = requests.get(INVENTORY_API).json()
#        print(data)

#        print("after json")
#        print(type(data.json()))
        for i in range(len(data)):

            if microservice in data[i]["microservices"] and env ==  data[i]["environment"]:
                servers_running_ms.append(data[i]["vmname"])
#        return Response(json.dumps(data), mimetype='application/json')
    return dumps(servers_running_ms), 200, {'Content-Type': 'application/json'}

@app.route('/api/kernel_patch', methods=[ 'GET', 'POST'])
def kernel_patch():
    if request.method == 'GET':
        data = mongo.db.patch.find({}, {'_id': False})
        return dumps(data), 200, {'Content-Type': 'application/json'}
    data = request.get_json()
    if request.method == 'POST':
        db_response = mongo.db.patch.delete_many({})
        mongo.db.patch.insert_one(data)
        return jsonify({'ok': True, 'message': 'Version updated!'}), 200

@app.route('/api/inventory', methods=['GET', 'POST', 'DELETE'])
def inventory():

    if request.method == 'GET':
        query = request.args
        data = mongo.db.inventory.find({}, {'_id': False})
        return dumps(data), 200, {'Content-Type': 'application/json'}
    data = request.get_json()
    if request.method == 'POST':
        if data.get('vmname', None) is not None:
            if "." not in str(data["vmname"]):
                data["vmname"]=data["vmname"]+".ic.ing.net"
            #deleting old stuff
            payload = {'vmname': data['vmname']}
            headers = {'content-type': 'application/json'}
            r = requests.delete("http://localhost:5001/api/inventory", json=payload, headers=headers)
            #inserting the new document
            now = datetime.datetime.now()
            data["last_alive_signal"]= now.strftime("%Y/%m/%d %H:%M:%S")
            mongo.db.inventory.insert_one(data)
            ES_ID=uuid.uuid1()
            es.index(index=ES_INDEX, doc_type=ES_MAPPING, id=ES_ID, body=data)
            return jsonify({'ok': True, 'message': 'Server added successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('vmname', None) is not None:
            db_response = mongo.db.inventory.delete_many({'vmname': data['vmname']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
