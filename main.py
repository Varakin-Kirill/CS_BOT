import logging
import asyncio
from aiogram import Bot, Dispatcher
import logging
import os
from handlers import master 
import handlers.reserve_handler as reserve_handler, handlers.start_handler as start_handler
from dotenv import load_dotenv
import threading
from schedules import schedules

logging.basicConfig(level=logging.INFO)

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.environ.get("BOT_TOKEN"))


async def main():
    dp.include_router(start_handler.router)
    dp.include_router(master.router)
    dp.include_router(reserve_handler.router)
    scheduler_thread = threading.Thread(target=schedules)
    scheduler_thread.start()
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())
