import psycopg2
import os
class DataBase():
    def __init__(self):
        print(os.getenv("PASSWORD"))
        self.connection = psycopg2.connect(
            dbname = os.getenv("DB_NAME"), 
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD"),
            host = os.getenv("HOST"),
            port = os.getenv("PORT"),
        )
    
    def insert_reserve(self, tg_id, name, surname, phone, amount, date, time):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO reserve (user_tg_id, name, surname, phone, amount, date, time)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""", (tg_id, name, surname, phone, amount , date, time))