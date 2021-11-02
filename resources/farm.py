from flask_restful import Resource, request
from config.db import db
import json
from bson import json_util, ObjectId
from flask_cors import cross_origin

farm_aggregation = [{"$lookup":{"from":'stats',"localField":"workers.id","foreignField":"rig_id","as":'stats'}},{"$project":{"inter":{"$map":{"input":"$workers","as":"one","in":{"$mergeObjects":["$$one",{"$arrayElemAt":[{"$filter":{"input":"$stats","as":"two","cond":{"$eq":["$$two.rig_id","$$one.id"]}}},0]}]}}}, "name": 1}},{"$lookup":{"from":"hardwares","localField":"inter.rig_id","foreignField":"rig_id","as":"hardwares"}},{"$project":{"workers":{"$map":{"input":"$inter","as":"one","in":{"$mergeObjects":["$$one",{"$arrayElemAt":[{"$filter":{"input":"$stats","as":"two","cond":{"$eq":["$$two.rig_id","$$one.id"]}}},0]}]}}}, "name": 1}}]


class Farm(Resource):

    def get(self, id=""):
        if id == "":
            farms = db.farms.aggregate(farm_aggregation[:3])
            farms = json.loads(json_util.dumps(farms))
            return farms, 200
        else:
            farm_match = {"$match": {"_id": ObjectId(id)}}
            farm = db.farms.aggregate([farm_match, *farm_aggregation])
            farm = json.loads(json_util.dumps(farm))[0]
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
