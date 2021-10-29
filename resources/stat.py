from flask_restful import Resource
from config.db import db
from bson import json_util
import json


class Stat(Resource):

    def get(self, rig_id):
        try:
            rig_id = int(rig_id)
        except:
            return {"error": "rig_id must be a number"}, 500

        stat = db.stats.find_one({
            "rig_id": rig_id
        })
        stat = json.loads(json_util.dumps(stat))
        return stat, 200
