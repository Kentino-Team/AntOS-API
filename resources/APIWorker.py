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
            db.hardwares.update_one({
                "rig_id": rig_id
            }, {"$set": {"rig_id": rig_id, "hardwares": request.json['params']}}, True)

            config = db.config.aggregate(
                [{"$match": {"rig_id": rig_id}}, {"$set": {"fs_id": {"$toObjectId": "$flightsheet"}}},
                 {"$lookup": {"from": "flightsheets", "localField": "fs_id", "foreignField": "_id", "as": "fs"}},
                 {"$project": {"fs": {"$arrayElemAt": ["$fs", 0]}, "rig_id": 1, "autofan": 1, "oc_template": 1}}])
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
                    "wallet": self.generate_wallet(rig_id, farm, config),
                    "autofan": self.generate_autofan(config),
                    "amd_oc": self.generate_amd_oc(config),
                    "nvidia_oc": self.generate_nvidia_oc(config)
                },
                "id": None
            }
            return resp, 200
        if method == 'stats':
            data = request.get_json(force=True)
            rig_id = int(request.args.get('id_rig'))
            password = data['params']['passwd']
            farm = self.hello(rig_id, password)
            if farm is None:
                return {'error': 'rig not found'}, 404
            db.stats.update_one({
                "rig_id": rig_id
            }, {
                "$set": {
                    "rig_id": rig_id,
                    "timestamp": datetime.now(),
                    "stats": data['params']
                }
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

            config = db.config.aggregate(
                [{"$match": {"rig_id": rig_id}}, {"$set": {"fs_id": {"$toObjectId": "$flightsheet"}}},
                 {"$lookup": {"from": "flightsheets", "localField": "fs_id", "foreignField": "_id", "as": "fs"}},
                 {"$project": {"fs": {"$arrayElemAt": ["$fs", 0]}, "rig_id": 1, "autofan": 1, "oc_template": 1}}])
            config = json.loads(json_util.dumps(config))

            if command['command'] == 'config':
                command.update({
                    "config": self.generate_config(rig_id, password, farm, config),
                    "wallet": self.generate_wallet(rig_id, farm, config)
                })
            elif command['command'] == 'autofan':
                command.update({
                    "autofan": self.generate_autofan(config)
                })
            elif command['command'] == 'amd_oc':
                command.update({
                    "amd_oc": self.generate_amd_oc(config)
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
        base_config = "HIVE_HOST_URL=\"http://192.168.31.85\"\n" \
                      "API_HOST_URL=\"http://192.168.31.85\"\n" \
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

    def generate_wallet(self, rig_id, farm, config):
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

    def generate_autofan(self, config):
        if len(config) == 0:
            return "ENABLED=0"

        config = config[0]
        if "autofan" not in config:
            return "ENABLED=0"

        autofan = config['autofan']

        return f"ENABLED={1 if autofan['enabled'] else 0}\n" \
               f"TARGET_TEMP={autofan['targetCoreTemp']}\n" \
               f"TARGET_MEM_TEMP={autofan['targetMemTemp']}\n" \
               f"MIN_FAN={autofan['minFanSpeed']}\n" \
               f"MAX_FAN={autofan['maxFanSpeed']}\n" \
               f"CRITICAL_TEMP={autofan['criticalTemp']}\n" \
               f"CRITICAL_TEMP_ACTION=\"\"\n" \
               f"NO_AMD={1 if autofan['noAmd'] else 0}\n" \
               f"REBOOT_ON_ERROR={1 if autofan['rebootOnError'] else 0}\n" \
               f"SMART_MODE={1 if autofan['smartMode'] else 0}\n"

    def generate_amd_oc(self, config):

        if len(config) == 0:
            return ""

        config = config[0]

        if config['oc_template'] == '':
            return ''

        oc = db.oc_templates.find({
            "_id": ObjectId(config['oc_template'])
        })
        oc = json.loads(json_util.dumps(oc))

        oc = oc['amd']

        return f"CORE_CLOCK=\"{oc['cc']}\"\n" \
               f"CORE_STATE=\"{oc['cs']}\"\n" \
               f"CORE_VDDC=\"{oc['cv']}\"\n" \
               f"MEM_CLOCK=\"{oc['mc']}\"\n" \
               f"MEM_STATE=\"{oc['ms']}\"\n" \
               f"MVDD=\"{oc['mv']}\"\n" \
               f"VDDCI=\"{oc['mcv']}\"\n" \
               f"FAN=\"{oc['fan']}\"\n" \
               f"PL=\"{oc['pw']}\"\n" \
               "REF=\"\"\n" \
               f"SOCCLK=\"{oc['soc_f']}\"\n" \
               f"SOCVDDMAX=\"{oc['vddmax']}\"\n" \
               f"AGGRESSIVE={1 if oc['aggressive_undervolting'] else 0}\n"

    def generate_nvidia_oc(self, config):

        if len(config) == 0:
            return ""

        config = config[0]

        if config['oc_template'] == '':
            return ''

        oc = db.oc_templates.find({
            "_id": ObjectId(config['oc_template'])
        })
        oc = json.loads(json_util.dumps(oc))

        oc = oc['nvidia']

        return f"CLOCK=\"{oc['cco']}\"\n" \
               f"MEM=\"{oc['mc']}\"\n" \
               f"FAN=\"{oc['fan']}\"\n" \
               f"PLIMIT=\"{oc['pw']}\"\n"
