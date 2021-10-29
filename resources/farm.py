from flask_restful import Resource
from config.db import db
import json
from bson import json_util, ObjectId


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

    def merge_work_stats(self, farms):
        for idxf, farm in enumerate(farms):
            for idxs, stats in enumerate(farm['stats']):
                rig_id = stats['rig_id']
                for idxw, worker in enumerate(farm['workers']):
                    id = worker['id']
                    if rig_id == id:
                        farms[idxf]['workers'][idxw] |= stats
            del farms[idxf]['stats']
        return farms
