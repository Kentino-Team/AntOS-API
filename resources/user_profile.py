from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from config.db import db
from bson import ObjectId


class UserProfile(Resource):

    @jwt_required()
    def put(self):
        user_id = current_identity.id
        username = request.json['username']
        fullname = request.json['fullname']
        email = request.json['email']

        db.users.update({
            "_id": ObjectId(user_id)
        }, {
            "$set": {
                "username": username,
                "fullname": fullname,
                "email": email
            }
        }, False)
        return {}, 200
