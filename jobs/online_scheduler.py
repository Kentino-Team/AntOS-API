import datetime
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from config.db import db


def check_for_online():
    now = datetime.datetime.now()
    limit = now - datetime.timedelta(minutes=5)
    stats = db.stats.find({"timestamp": {"$gt": limit}})
    print(stats)


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_for_online, trigger="interval", seconds=3)


def start_scheduler():
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
