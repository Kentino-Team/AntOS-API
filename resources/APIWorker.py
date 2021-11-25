from flask_restful import Resource
from flask import request
from config.db import db
from bson import json_util
from bson.objectid import ObjectId
import json
from datetime import datetime


class APIWorker(Resource):

    def post(self):
        if not all(k in request.args.keys() for k in ('id_rig', 'method')):
            return {}, 200

        rig_id = int(request.args.get('id_rig'))
        method = request.args.get('method')

        if method == 'hello':
            password = request.json['params']['passwd']
            farm = self.hello(rig_id, password)
            if farm is None:
                return {'error': 404, 'message': 'no worker found'}, 404
            db.hardwares.update({
                "rig_id": rig_id
            }, {"rig_id": rig_id, "hardwares": request.json['params']}, True)
            resp = {
                "jsonrpc": "2.0",
                "result": {
                    "rig_name": farm['workers'][0]['name'],
                    "repository_list": "deb http://vicart.ovh:8081/repository/AntOS_APT/ bionic main\n"
                                       "deb http://vicart.ovh:8081/repository/AntOS_APT_Proxy bionic main\n"
                                       "deb-src http://cz.archive.ubuntu.com/ubuntu/ bionic main\n",
                    "config": self.generate_config(rig_id, password, farm),
                    "wallet": self.generate_wallet(rig_id, farm),
                    "autofan": "en"
                },
                "id": None
            }
            return resp, 200
        if method == 'stats':
            data = request.get_json(force=True)
            rig_id = int(request.args.get('id_rig'))
            password = data['params']['passwd']
            if self.hello(rig_id, password) is None:
                return {'error': 'rig not found'}, 404
            db.stats.update({
                "rig_id": rig_id
            }, {
                "rig_id": rig_id,
                "timestamp": datetime.now(),
                "stats": data['params']
            }, True)
            command = db.commands.find_one({
                "rig_id": rig_id,
                "run": False
            }, {
                "rig_id": 0,
                "run": 0
            })
            if command is None:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "command": "OK"
                    }
                }, 200

            command = json.loads(json_util.dumps(command))

            db.commands.delete_one({
                "_id": ObjectId(command['_id']['$oid'])
            })
            return {
                "jsonrpc": "2.0",
                "result": command
            }, 200
        if method == 'message':
            print(request.json)
        return {"data": "error"}, 200

    def hello(self, rig_id, passwd):
        worker = db.farms.find_one({
            "workers.id": rig_id,
            "workers.pwd": passwd
        }, {
            "name": 1,
            "workers": {"$elemMatch": {"id": rig_id, "pwd": passwd}}
        })
        if worker is None or 'workers' not in worker:
            return None
        return worker

    def generate_config(self, rig_id, passwd, farm):
        return "HIVE_HOST_URL=\"http://172.29.128.1\"\n" \
               "API_HOST_URL=\"http://172.29.128.1\"\n" \
               f"RIG_ID={rig_id}\n" \
               f"RIG_PASSWD=\"{passwd}\"\n" \
               f"WORKER_NAME=\"{farm['workers'][0]['name']}\"\n" \
               f"FARM_ID={farm['_id']}\n" \
               "TIMEZONE=\"Europe/Prague\"\n" \
               "WD_ENABLED=0\n" \
               "MINER=\"nanominer\""

    def generate_wallet(self, rig_id, farm):
        return "NANOMINER_ALGO=\"ethash\"\n" \
               "NANOMINER_TEMPLATE=\"0x011ABFc17beFb8270398F0CC99801E326B8B13D8\"\n" \
               "NANOMINER_URL=\"eu-eth.hiveon.net:4444 eu-eth.hiveon.net:14444\"\n" \
               "NANOMINER_PASS=\"x\"\n" \
               "NANOMINER_USER_CONFIG=\"coin = ETH\nrigName = Rig_rrrr\"\n" \
               "META='{\"nanominer\": {\"coin\": \"ETH\"}}'"
