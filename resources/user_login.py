from flask_restful import Resource, request
from config.db import db


class UserLogin(Resource):

    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        db.users.insert_one({
            "username": username,
            "email": email,
            "pwd": password
        })
        return {}, 201

    def options(self):
        return 200
