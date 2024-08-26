import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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
    
    def get_items(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""select item_id, name, price from items""")
                return cursor.fetchall()
            
    
    
    def get_master_data(self, master_id, duty_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""with ts as (select opened_at, coalesce(closed_at, now()) as closed_at from duties where id = %s) 
            select sum(100), count(*) 
                    from items_purchased T 
                        left join items 
                               on items.item_id = T.item_id 
                    where T.master = %s
                               and T.item_id < 5 
                               and created_at < (select closed_at from ts) 
                               and created_at >= (select opened_at from ts)""", (duty_id, master_id, ))
                return cursor.fetchone()
            
    def insert_buy(self, item_id, master_id, payment, comment):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""insert into items_purchased (item_id, master, amount, comment, payment) values(%s, %s, 1, %s, %s)""", (item_id, master_id, comment, payment,))


    def get_hookah_master(self, tg_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""select user_id from masters where tg_id = %s""", (tg_id,))
                rows = cursor.fetchone()
                if rows is not None:
                    return rows[0]
                else:
                    return None
                
    def open_duty(self, master_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""insert into duties (master) values (%s)""", (master_id,))

    def get_active_duty(self):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""select id, master from duties where closed_at is null""")
                return cursor.fetchone()


    def close_duty(self, master_id, duty_id):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""update duties set closed_at = now() where id = %s and master = %s""", (duty_id, master_id,))

    def validate_reserve(self, tg_id, name, surname, phone, amount, date, time):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO reserve (user_tg_id, name, surname, phone, amount, date, time)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""", (tg_id, name, surname, phone, amount , date, time))
                
    def insert_reserve(self, tg_id, name, surname, phone, amount, date, time):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO reserve (user_tg_id, name, surname, phone, amount, date, time)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""", (tg_id, name, surname, phone, amount , date, time))