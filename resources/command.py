import json
from bson import json_util
from flask_restful import Resource
from config.db import db
from flask import request
from flask_cors import cross_origin, CORS
from flask_jwt import jwt_required, current_identity


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
