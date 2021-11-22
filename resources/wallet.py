from flask_restful import Resource, request
from flask_jwt import jwt_required, current_identity
from config.db import db
import json
from bson import json_util


class Wallet(Resource):

    @jwt_required()
    def get(self, id=""):
        user_id = current_identity.id
        global wallets
        if id == "":
            wallets = db.wallets.find({
                "user_id": user_id,
                "farm_id": ""
            })
        else:
            wallets = db.wallets.find({
                "user_id": user_id,
                "farm_id": {
                    "$in": ["", id]
                }
            })
        wallets = json.loads(json_util.dumps(wallets))
        return wallets, 200

    @jwt_required()
    def post(self, id=""):
        user_id = current_identity.id
        wallet = request.json["wallet"]
        wallet.update({
            "user_id": user_id,
            "farm_id": "" if id == "null" else id
        })
        db.wallets.insert_one(wallet)
        return {}, 200

    @jwt_required()
    def delete(self):
        user_id = current_identity.id
        wallet_address = request.args.get("wallet_address")
        db.wallets.delete_one({
            "user_id": user_id,
            "address": wallet_address
        })
        return {}, 200
