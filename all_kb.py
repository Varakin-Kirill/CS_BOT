from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

confirm_buttons = [
    [KeyboardButton(text="подтвердить"),KeyboardButton(text="начать сначала")]
]

confirm_kb = ReplyKeyboardMarkup(
    keyboard= confirm_buttons,
    resize_keyboard=True
)

start_buttons = [
    [KeyboardButton(text="забронировать столик")]
]

start_kb = ReplyKeyboardMarkup(
    keyboard= start_buttons,
    resize_keyboard=True
)