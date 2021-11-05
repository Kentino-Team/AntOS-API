from flask_jwt import JWT, current_identity
from config.db import db
from bson import ObjectId, json_util
from flask import Flask
import json
from models.User import User


def auth(username, password):
    user = db.users.find_one({
        "username": username,
        "pwd": password
    })
    if user is None:
        return None
    user = json.loads(json_util.dumps(user))
    user = User(user['_id']['$oid'], user['username'], user['pwd'])
    return user


def identity(payload):
    userid = payload['identity']
    user = db.users.find_one({
        "_id": ObjectId(userid)
    })
    if user is None:
        return None
    user = json.loads(json_util.dumps(user))
    user = User(user['_id']['$oid'], user['username'], user['pwd'])
    return user


def init_jwt(app: Flask):
    app.config['SECRET_KEY'] = 'teset'
    app.config['JWT_AUTH_URL_RULE'] = '/user/login'
    JWT(app, auth, identity)
