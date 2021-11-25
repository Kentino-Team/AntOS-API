from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util
from flask_cors import cross_origin


class Config(Resource):

    def get(self, rig_id=""):
        rig_id = int(rig_id)
        config = db.config.find_one({
            "rig_id": rig_id
        })
        config = json.loads(json_util.dumps(config))
        return config, 200

    def post(self, rig_id=""):
        rig_id = int(rig_id)
        fs = request.json['fs_id']
        db.config.update({
            "rig_id": rig_id
        }, {
            "rig_id": rig_id,
            "flightsheet": fs
        }, True)
        return {}, 200

    @cross_origin()
    def options(self):
        return 200
