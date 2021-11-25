from pymongo import MongoClient
import json
from bson import json_util
from datetime import datetime, timedelta


def run_job():
    client = MongoClient('mongodb://admin:Xolider500_%40@vicart.ovh:27017/?authSource=admin')
    db = client.antos
    now = datetime.now()
    diff = now - timedelta(minutes=10)
    db.stats.delete_many({
        "timestamp": {
            "$lt": diff
        }
    })


if __name__ == '__main__':
    run_job()
