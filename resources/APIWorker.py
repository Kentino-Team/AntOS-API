from flask_restful import Resource
from flask import request
from config.db import db
from bson import json_util
from bson.objectid import ObjectId
import json
from datetime import datetime
from functools import reduce


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

            config = db.config.aggregate(
                [{"$match": {"rig_id": rig_id}}, {"$set": {"fs_id": {"$toObjectId": "$flightsheet"}}},
                 {"$lookup": {"from": "flightsheets", "localField": "fs_id", "foreignField": "_id", "as": "fs"}},
                 {"$project": {"fs": {"$arrayElemAt": ["$fs", 0]}, "rig_id": 1}}])
            config = json.loads(json_util.dumps(config))

            resp = {
                "jsonrpc": "2.0",
                "result": {
                    "rig_name": farm['workers'][0]['name'],
                    "repository_list": "#deb http://vicart.ovh:8081/repository/antos bionic main\n"
                                       "deb http://vicart.ovh:8081/repository/antos-proxy bionic main\n"
                                       "deb-src http://cz.archive.ubuntu.com/ubuntu/ bionic main\n"
                                       "deb http://download.hiveos.farm/repo/binary/ /",
                    "config": self.generate_config(rig_id, password, farm, config),
                    "wallet": self.generate_wallet(config, farm),
                    "autofan": self.generate_autofan(),
                    "amd_oc": self.generate_amd_oc()
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

    def generate_config(self, rig_id, passwd, farm, config):
        base_config = "HIVE_HOST_URL=\"http://192.168.88.59\"\n" \
                      "API_HOST_URL=\"http://192.168.88.59\"\n" \
                      f"RIG_ID={rig_id}\n" \
                      f"RIG_PASSWD=\"{passwd}\"\n" \
                      f"WORKER_NAME=\"{farm['workers'][0]['name']}\"\n" \
                      f"FARM_ID={farm['_id']}\n" \
                      "TIMEZONE=\"Europe/Prague\"\n" \
                      "WD_ENABLED=0\n"

        if len(config) == 0:
            return base_config
        config = config[0]
        base_config += f"MINER=\"{config['fs']['miner']['name']}\""
        return base_config

    def generate_wallet(self, config, farm):
        if len(config) == 0:
            return ""

        config = config[0]
        wallet = db.wallets.find_one({
            "_id": ObjectId(config['fs']['wallet_id']['$oid'])
        })
        config.update({"wallet": wallet})

        miner = config['fs']['miner']['name']

        if miner == "nanominer":
            return f"NANOMINER_ALGO=\"{config['fs']['miner']['algo']}\"\n" \
                          f"NANOMINER_TEMPLATE=\"{self.parseTemplate(farm, config, config['fs']['miner']['wallet_template'])}\"\n" \
                          f"NANOMINER_URL=\"{self.parseTemplate(farm, config, config['fs']['miner']['pool_template'])}\"\n" \
                          f"NANOMINER_PASS=\"{config['fs']['miner']['pass']}\"\n" \
                          f"NANOMINER_USER_CONFIG=\"{self.parseTemplate(farm, config, config['fs']['miner']['extra'])}\"\n" \
                          "META='{\"" + config['fs']['miner']['name'] + "\": {\"coin\": \"" + config['fs']['coin'] + "\"}}'"
        elif miner == "phoenixminer":
            return f"PHOENIXMINER_URL=\"{self.parseTemplate(farm, config, config['fs']['miner']['wallet_template'])}\"\n" \
                   f"PHOENIXMINER_USER_CONFIG='{self.parseTemplate(farm, config, config['fs']['miner']['extra'])}'\n" \
                   "META='{\"" + config['fs']['miner']['name'] + "\": {\"coin\": \"" + config['fs']['coin'] + "\"}}'"

        return ""

    def parseTemplate(self, farm, config, str):
        return str.replace('%WAL%', config['wallet']['address']).replace('%WORKER_NAME%', farm['workers'][0]['name']) \
            .replace('%URL%', reduce(lambda old, new: old + new + "\n", config['fs']['pool']['urls'])) \
            .replace('%COIN%', config['fs']['coin'])

    def generate_autofan(self):
        return "ENABLED=1\n" \
               "TARGET_TEMP=85\n" \
               "TARGET_MEM_TEMP=90\n" \
               "MIN_FAN=65\n" \
               "MAX_FAN=100\n" \
               "CRITICAL_TEMP=90\n" \
               "CRITICAL_TEMP_ACTION=\"\"\n" \
               "NO_AMD=\n" \
               "REBOOT_ON_ERROR=\n" \
               "SMART_MODE=\n"

    def generate_amd_oc(self):
        return "CORE_CLOCK=\"1044\"\n" \
               "CORE_STATE=\"1\"\n" \
               "CORE_VDDC=\"850\"\n" \
               "MEM_CLOCK=\"1900\"\n" \
               "MEM_STATE=\"1\"\n" \
               "MVDD=\"850\"\n" \
               "VDDCI=\"850\"\n" \
               "FAN=\"64\"\n" \
               "PL=\"\"\n" \
               "REF=\"20\"\n" \
               "SOCCLK=\"\"\n" \
               "SOCVDDMAX=\"\"\n" \
               "AGGRESSIVE=1\n"
