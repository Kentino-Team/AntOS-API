from flask_restful import Resource
from config.db import db
from flask import request
from flask_cors import cross_origin, CORS


class Command(Resource):

    def post(self):
        command = request.json['command']
        rig_id = int(request.args.get('id_rig'))

        db.commands.insert_one({
            "rig_id": rig_id,
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
