from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from db import DataBase

db = DataBase()

confirm_buttons = [
    [KeyboardButton(text="Подтвердить"),KeyboardButton(text="Начать сначала")]
]

confirm_kb = ReplyKeyboardMarkup(
    keyboard= confirm_buttons,
    resize_keyboard=True
)

start_buttons = [
    [KeyboardButton(text="Забронировать столик"), KeyboardButton(text="Мои бронирования")]
]

start_kb = ReplyKeyboardMarkup(
    keyboard= start_buttons,
    resize_keyboard=True
)

SELL = "Замутить продажу"
SEE_BOOKS = "Посмотреть брони"

master_buttons = [
    [KeyboardButton(text=SELL), KeyboardButton(text=SEE_BOOKS)]
]

master_kb = ReplyKeyboardMarkup(
    keyboard= master_buttons,
    resize_keyboard=True
)

class ItemCallback(CallbackData, prefix="item"):
    item_id: int

def select_item_buttons():
    items = db.get_items()
    all_items = [InlineKeyboardButton(text=data[1], callback_data=ItemCallback(item_id=data[0]).pack()) for data in items]
    return [all_items[i * 2:(i + 1) * 2] for i in range((len(all_items) + 2 - 1) // 2 )] 

def select_item_markup(items):
    return InlineKeyboardMarkup(
    inline_keyboard=items,
    resize_keyboard=True,
)