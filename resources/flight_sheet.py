from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from flask_cors import cross_origin
from config.db import db
import json
from bson import json_util, ObjectId


class FlightSheet(Resource):

    @jwt_required()
    def get(self, id=""):
        user_id = current_identity.id
        global flight_sheets
        if id == "":
            flight_sheets = db.flightsheets.aggregate([
                {
                    "$match": {
                        "user_id": user_id,
                        "farm_id": ""
                    }
                },
                {
                    "$lookup": {
                        "from": "wallets",
                        "localField": "wallet_id",
                        "foreignField": "_id",
                        "as": "wallet"
                    }
                }
            ])
        else:
            flight_sheets = db.flightsheets.aggregate([
                {
                    "$match": {
                        "user_id": user_id,
                        "farm_id": {
                            "$in": ["", id]
                        }
                    }
                },
                {
                    "$lookup": {
                        "from": "wallets",
                        "localField": "wallet_id",
                        "foreignField": "_id",
                        "as": "wallet"
                    }
                }
            ])
        flight_sheets = json.loads(json_util.dumps(flight_sheets))
        return flight_sheets, 200

    @jwt_required()
    def post(self, id=""):
        fs = request.json['fs']
        fs.update({"wallet_id": ObjectId(fs['wallet_id']), "user_id": current_identity.id, "farm_id": id})
        db.flightsheets.insert_one(fs)
        return {}, 201

    @jwt_required()
    def delete(self):
        fs = request.args['fs']
        db.flightsheets.delete_one({
            "user_id": current_identity.id,
            "_id": ObjectId(fs)
        })
        return {}, 200

    @cross_origin()
    def options(self):
        return 200

