from flask_restful import Resource
from config.db import db
import json
from bson import json_util


class Miner(Resource):

    def get(self):
        miners = db.miners.find()
        miners = json.loads(json_util.dumps(miners))
        return miners, 200
