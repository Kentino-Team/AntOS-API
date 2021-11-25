from flask_restful import Resource
from config.db import db
import json
from bson import json_util


class Pools(Resource):

    def get(self):
        pools = db.pools.find()
        pools = json.loads(json_util.dumps(pools))
        return pools, 200