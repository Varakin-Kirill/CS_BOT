import logging
import asyncio
from aiogram import Bot, Dispatcher
import logging
import os
import handlers.reserve_handler as reserve_handler, handlers.start_handler as start_handler, handlers.master_handler as master_handler
from dotenv import load_dotenv
import threading
from close_duties import close_duties

logging.basicConfig(level=logging.INFO)

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.environ.get("BOT_TOKEN"))


async def main():
    dp.include_router(start_handler.router)
    dp.include_router(reserve_handler.router)
    dp.include_router(master_handler.router)
    scheduler_thread = threading.Thread(target=close_duties)
    scheduler_thread.start()
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())
