from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from state_list import reserve_form
from all_kb import confirm_kb
from db import DataBase

router = Router()

db = DataBase()
@router.message(F.text == "забронировать столик")
async def form(message: Message, state : FSMContext):
    await message.answer("Введите имя:")
    await state.set_state(reserve_form.name)
    
@router.message(reserve_form.name)
async def name(message: Message, state : FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите фамилию:")
    await state.set_state(reserve_form.surname)
    
@router.message(reserve_form.surname)
async def surname(message: Message, state : FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(reserve_form.phone)
    
@router.message(reserve_form.phone)
async def phone(message: Message, state : FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите кол-во человек:")
    await state.set_state(reserve_form.amount)

@router.message(reserve_form.amount)
async def amount(message: Message, state : FSMContext):
    await state.update_data(amount=message.text)
    await message.answer("Введите дату брони:")
    await state.set_state(reserve_form.date)

@router.message(reserve_form.date)
async def date(message: Message, state : FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите время брони:")
    await state.set_state(reserve_form.date)

@router.message(reserve_form.time)
async def time(message: Message, state : FSMContext):
    await state.update_data(time=message.text)
    await update_on_reject(message, state)
    await state.set_state(reserve_form.confirm)
        
async def update_on_reject(message: Message, state: FSMContext): 
    data = await state.get_data()
    await message.answer(
        (   
            f"Ваш данные указанные выше:\n"
            f"<b>Имя</b>: {data['name']}\n"
            f"<b>Фамилия</b>: {data['surname']}\n" 
            f"<b>Номер телефона</b>: {data['phone']}\n"
            f"<b>кол-во человек</b>: {data['amount']}\n"
            f"<b>Дата брони</b>: {data['date']}\n"
            f"<b>Время брони</b>: {data['time']}\n"
        ),
        parse_mode="HTML",
        reply_markup=confirm_kb
    )

@router.message( F.text=="подтвердить", reserve_form.confirm)
async def confirm_handler(message : types.Message, state : FSMContext):
    data = await state.get_data()
    await message.answer("Спасибо за вашу форму!")
    db.insert_reserve(message.from_user.id, data['name'], data['surname'], data['phone'], data['amount'], data['date'], data['time'] )
    await state.clear()


    
    
