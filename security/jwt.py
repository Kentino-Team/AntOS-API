from flask_jwt import JWT, current_identity
from config.db import db
from bson import ObjectId, json_util
from flask import Flask
import json


def auth(username, password):
    user = db.users.find_one({
        "username": username,
        "pwd": password
    })
    user['id'] = str(user['_id'])
    return user


def identity(payload):
    print(payload)
    userid = payload['identity']
    user = db.users.find_one({
        "_id": ObjectId(userid)
    })
    user = json.loads(json_util.dumps(user))
    user.update({id: user['_id']['$oid']})
    return user


def init_jwt(app: Flask):
    app.config['SECRET_KEY'] = 'teset'
    app.config['JWT_AUTH_URL_RULE'] = '/user/login'
    JWT(app, auth, identity)
