from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from all_kb import start_kb


router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("тут будет описание сервиса", reply_markup=start_kb)