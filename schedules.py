import schedule
import time
from db import DataBase
import logging

db = DataBase()


def schedules():
    schedule.every().day.at("03:00", "Asia/Omsk").do(db.close_duty)
    schedule.every().month.at("03:00", "Asia/Omsk").do(db.close_duty)
    while True:
        schedule.run_pending()
        time.sleep(1)

