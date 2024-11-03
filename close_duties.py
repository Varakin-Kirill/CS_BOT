import schedule
import time
from db import DataBase
import logging
import pytz

db = DataBase()


def close_duties():
    schedule.every().day.at("03:00", "Asia/Omsk").do(db.close_duty)

    while True:
        schedule.run_pending()
        time.sleep(1)
