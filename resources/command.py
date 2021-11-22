from flask_restful import Resource
from config.db import db
from flask import request
from flask_cors import cross_origin, CORS
from flask_jwt import jwt_required


class Command(Resource):

    @jwt_required()
    def post(self, rig=""):
        command = request.json['command']

        db.commands.insert_one({
            "rig_id": int(rig),
            "command": "batch",
            "commands": [
                {
                    "command": "exec",
                    "exec": command
                }
            ]
        })
        return 200

    @cross_origin()
    def options(self):
        return 200
