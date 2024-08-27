import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
import logging
import os
import main_handler, start, master_handler
from dotenv import load_dotenv
import threading
from close_duties import close_duty

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.environ.get("BOT_TOKEN"))

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(start.router)
    dp.include_router(main_handler.router)
    dp.include_router(master_handler.router)
    await dp.start_polling(bot, skip_updates=False)
    scheduler_thread = threading.Thread(target=close_duty)
    scheduler_thread.start()


if __name__ == "__main__":
    asyncio.run(main())
