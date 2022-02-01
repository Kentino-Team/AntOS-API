import json

import pymongo
from bson import json_util
from flask_restful import Resource
from config.db import db
from flask import request
from flask_cors import cross_origin, CORS
from flask_jwt import jwt_required, current_identity
from datetime import datetime


class Command(Resource):

    @jwt_required()
    def post(self, rig=""):
        command = request.json['command']

        rig_owner = db.farms.find_one({
            "workers.id": int(rig)
        })
        rig_owner = json.loads(json_util.dumps(rig_owner))
        if rig_owner['user_id'] != current_identity.id:
            return {"error": "forbidden"}, 403

        base_command = {
            "rig_id": int(rig),
            "timestamp": datetime.now()
        }

        if command == "batch":
            command_parameter = request.json['command_parameter']
            base_command.update({
                "command": "batch",
                "commands": [
                    {
                        "command": "exec",
                        "exec": command_parameter
                    }
                ]
            })
        else:
            base_command.update({
                "command": command
            })

        base_command.update({
            "run": False
        })

        db.commands.insert_one(base_command)
        return 200

    @jwt_required()
    def get(self, rig=""):
        rig_owner = db.farms.find_one({
            "workers.id": int(rig)
        })
        rig_owner = json.loads(json_util.dumps(rig_owner))
        if rig_owner['user_id'] != current_identity.id:
            return {"error": "forbidden"}, 403

        commands = db.commands.find({
            "rig_id": int(rig)
        }).sort([("timestamp", pymongo.DESCENDING)]).limit(10)
        commands = json.loads(json_util.dumps(commands))
        return commands, 200

    @cross_origin()
    def options(self):
        return 200
