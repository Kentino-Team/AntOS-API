import string
from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util, ObjectId
import random
from flask_jwt import jwt_required, current_identity


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
                    "lastId": {
                        "$max": "$workers.id"
                    }
                }
            }
        ])
        last_id = json.loads(json_util.dumps(total_workers))[0]["lastId"]
        new_worker = last_id+1

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        db.farms.update({"_id": ObjectId(farm_id)}, {"$addToSet": {"workers": {
            "name": "no_name",
            "id": new_worker,
            "pwd": password
        }}})
        return {"id": new_worker, "pwd": password}, 200

    @jwt_required()
    def delete(self, rig_id=""):
        rig_id = int(rig_id)
        update_result = db.farms.update_one({
            "user_id": current_identity.id,
            "workers.id": rig_id
        }, {
            "$pull": {
                "workers": {
                    "id": rig_id
                }
            }
        })
        if update_result.matched_count > 0:
            db.config.delete_one({
                "rig_id": rig_id
            })
            db.hardwares.delete_one({
                "rig_id": rig_id
            })
            db.stats.delete_one({
                "rig_id": rig_id
            })
        return {}, 200

    @jwt_required()
    def put(self, rig_id=""):
        rig_id = int(rig_id)
        name = request.json['name']
        pwd = request.json['password']
        db.farms.update_one({
            "user_id": current_identity.id,
            "workers.id": rig_id
        }, {
            "$set": {
                "workers.$.name": name,
                "workers.$.pwd": pwd
            }
        })
        return {}, 200

    def options(self, rig_id=""):
        return 200
