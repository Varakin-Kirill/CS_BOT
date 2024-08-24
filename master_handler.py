from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from state_list import reserve_form
from all_kb import confirm_kb
from db import DataBase
from all_kb import SELL, select_item_markup, select_item_buttons, ItemCallback, master_kb
from aiogram.filters import Command

router = Router()

db = DataBase()

@router.message(Command("open_duty"))
async def open_duty(message: Message, state : FSMContext):
    master_id = db.get_hookah_master(message.from_user.id)
    if master_id is not None:
        try:
            db.open_duty(master_id)
            await state.update_data(master_id=master_id)
            await message.answer("Удачной сменки", reply_markup=master_kb)
        except:
            await message.answer("А ты че нахуй, не твоя смена, съебал отсюда")
    else:
        await message.answer("Пошел нахуй отсюда")

@router.message(F.text == SELL)
async def select_item(message: Message, state : FSMContext):
    buttons = select_item_buttons()
    print(await state.get_state())
    print(buttons)
    markup = select_item_markup(buttons)
    await message.answer("Обоснуй че продал", reply_markup=markup)
    

@router.callback_query(ItemCallback.filter())
async def apply_item(query: CallbackQuery, state : FSMContext):
    master_id = await state.get_data()["master_id"]
    db.insert_buy(1, master_id)
    await query.message.answer("Ок понял братик")
