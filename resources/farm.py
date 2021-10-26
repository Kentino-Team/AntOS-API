from flask_restful import Resource
from config.db import db
import json
from bson import json_util


class Farm(Resource):

    def get(self):
        farms = db.farms.find()
        workers = db.stats.find()
        farms = json.loads(json_util.dumps(farms))
        workers = json.loads(json_util.dumps(workers))
        for i in range(0, len(farms)):
            for j in range(0, len(farms[i]['workers'])):
                worker_stat = [x for x in workers if workers[x]['rig_id'] == farms[i]['workers'][j]['id']]
                if len(worker_stat) > 0:
                    farms[i]['workers'][j]['stats'] = worker_stat[0]
        print(farms)
        return farms, 200
