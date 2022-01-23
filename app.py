import json
import random
from flask import Flask, jsonify, request
from bson import ObjectId
from markupsafe import re
from api.models import db

app = Flask(__name__)

def uniqueid():
    return int(random.randint(1, 1000000000))

unique_sequence = uniqueid()

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def index():
    result = list(db['blog'].find({}))
    return jsonify(JSONEncoder().encode(result)), 200

@app.route('/blogs')
def blogs():
    result = list(db['blog'].find({}))
    return jsonify(JSONEncoder().encode(result)), 200

@app.route('/blogs', methods=['POST'])
def createblog():
    fBlogs = list(db['blog'].find({}))
    id = uniqueid()
    if request.json['title'] and request.json['author'] and request.json['body']:
        for blog in fBlogs:
            if int(blog['id']) == id:
                id = uniqueid()
            elif blog == fBlogs[len(fBlogs)-1]:
                if int(blog['id']) == id:
                    id = uniqueid()
                addObj = request.json
                addObj['id'] = id
                db['blog'].insert_one(addObj)
                return jsonify('success'), 200
    else:
        return jsonify('not enough info'), 400

@app.route('/blogs/<id>')
def blogdets(id=0):
    if isInt(id):
        result = db['blog'].find_one({'id': int(id)})
        if result:
            return jsonify(JSONEncoder().encode(result)), 200
        else:
            return jsonify('not found'), 404
    return jsonify('not found'), 404

@app.route('/blogs/<id>', methods=['DELETE'])
def deleteblog(id=0):
    if isInt(id):
        result = db['blog'].find_one({'id': int(id)})
        if result:
            db['blog'].delete_one({'id': int(id)})
            return jsonify('deleted successfully'), 200
        else:
            return jsonify('not found'), 404
    return jsonify('not found'), 404

if __name__ == '__main__':
    app.run(debug=True)