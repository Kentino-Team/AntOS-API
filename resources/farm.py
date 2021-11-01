from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util, ObjectId
from flask_cors import cross_origin


class Farm(Resource):

    def get(self, id=""):
        if id == "":
            farms = db.farms.aggregate([{
                "$lookup": {
                    "from": 'stats',
                    "localField": "workers.id",
                    "foreignField": "rig_id",
                    "as": 'stats'
                }
            }])
            farms = json.loads(json_util.dumps(farms))
            farms = self.merge_work_stats(farms)
            return farms, 200
        else:
            farm = db.farms.aggregate([{
                "$match": {
                    "_id": ObjectId(id)
                }
            },
                {
                    "$lookup": {
                        "from": 'stats',
                        "localField": "workers.id",
                        "foreignField": "rig_id",
                        "as": 'stats'
                    }
                }])
            farm = json.loads(json_util.dumps(farm))
            farm = self.merge_work_stats(farm)[0]
            return farm, 200

    def post(self, id=""):
        if id != "":
            return {"error": "method not allowed"}, 405
        else:
            db.farms.insert_one(request.json)
            return {"message": "success"}, 201

    @cross_origin()
    def options(self):
        return 200

    def merge_work_stats(self, farms):
        for idxf, farm in enumerate(farms):
            for idxs, stats in enumerate(farm['stats']):
                rig_id = stats['rig_id']
                for idxw, worker in enumerate(farm['workers']):
                    id = worker['id']
                    if rig_id == id:
                        farms[idxf]['workers'][idxw].update(stats)
            del farms[idxf]['stats']
        return farms
