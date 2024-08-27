import schedule
import time
from db import DataBase

db = DataBase()


def close_duty():
    schedule.every().day.at("03:00").do(db.close_duty)
    while True:
        schedule.run_pending()
        time.sleep(1)
