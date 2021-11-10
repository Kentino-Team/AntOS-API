from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from config.db import db
import json
from bson import json_util


class Wallet(Resource):

    @jwt_required()
    def get(self):
        user_id = current_identity.id
        wallets = db.wallets.find({
            "user_id": user_id
        })
        wallets = json.loads(json_util.dumps(wallets))
        return wallets, 200
