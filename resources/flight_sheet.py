from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from config.db import db
import json
from bson import json_util


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
