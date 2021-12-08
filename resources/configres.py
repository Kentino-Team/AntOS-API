from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util
from flask_cors import cross_origin
from flask_jwt import jwt_required, current_identity


class Config(Resource):

    def get(self, rig_id=""):
        rig_id = int(rig_id)
        config = db.config.find_one({
            "rig_id": rig_id
        })
        config = json.loads(json_util.dumps(config))
        return config, 200

    @jwt_required()
    def post(self, rig_id=""):
        rig_id = int(rig_id)
        if not self.check_user(rig_id):
            return {}, 403

        type = request.args['type']
        if type == "fs":
            fs = request.json['fs_id']
            db.config.update_one({
                "rig_id": rig_id
            }, {
                "$set": {
                    "flightsheet": fs
                }
            }, True)
        elif type == "autofan":
            autofan = request.json['autofan']
            autofan['minFanSpeed'] = int(autofan['minFanSpeed'])
            autofan['maxFanSpeed'] = int(autofan['maxFanSpeed'])
            autofan['targetCoreTemp'] = int(autofan['targetCoreTemp'])
            autofan['targetMemTemp'] = int(autofan['targetMemTemp'])
            autofan['criticalTemp'] = int(autofan['criticalTemp'])
            db.config.update_one({
                "rig_id": rig_id
            }, {
                "$set": {
                    "autofan": autofan
                }
            })
        else:
            return {"error": "no type provided"}, 500
        return {}, 200

    @jwt_required()
    def delete(self, rig_id=""):
        rig_id = int(rig_id)
        if not self.check_user(rig_id):
            return {}, 403

        type = request.args['type']

        if type == "fs":
            db.config.update_one({
                "rig_id": rig_id
            }, {
                "$set": {
                    "flightsheet": None
                }
            })
        else:
            return {"error": "no type provided"}, 500
        return {}, 200

    @cross_origin()
    def options(self):
        return 200

    def check_user(self, rig_id):
        farm = db.farms.find_one({
            "workers.id": rig_id
        })
        if farm['user_id'] == current_identity.id:
            return True
        return False
