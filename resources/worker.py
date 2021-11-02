from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util, ObjectId


class Worker(Resource):

    def post(self):
        farm_id = request.json['farm_id']
        total_workers = db.farms.aggregate([
            {
                "$unwind": "$workers"
            },
            {
                "$group": {
                    "_id": None,
                    "workers": {
                        "$sum": 1
                    }
                }
            }
        ])
        total_workers = json.loads(json_util.dumps(total_workers))[0]["workers"]
        new_worker = total_workers+1
        db.farms.update({"_id": ObjectId(farm_id)}, {"$addToSet": {"workers": {
            "name": "",
            "id": new_worker,
            "pwd": "eeee"
        }}})
        return {"id": new_worker, "pwd": "eee"}, 200

    def options(self):
        return 200
