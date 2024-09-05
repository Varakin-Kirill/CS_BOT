from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from state_list import reserve_form
from all_kb import confirm_kb, get_phone_kb
from db import DataBase

router = Router()

db = DataBase()


@router.message(F.text == "Забронировать столик")
async def form(message: Message, state: FSMContext):
    await message.answer("Введите имя:")
    await state.set_state(reserve_form.name)


@router.message(reserve_form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите фамилию:")
    await state.set_state(reserve_form.surname)


# @router.message(reserve_form.surname)
# async def surname(message: Message, state: FSMContext):
#     await state.update_data(surname=message.text)
#     await message.answer("Введите кол-во человек:")
#     await state.set_state(reserve_form.phone)


@router.message(reserve_form.surname)
async def surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Отправтьте номер телефона ⬇️", reply_markup=get_phone_kb)
    await state.set_state(reserve_form.phone)


@router.message(F.contact, reserve_form.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Введите кол-во человек:")
    await state.set_state(reserve_form.amount)


@router.message(reserve_form.amount)
async def amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.answer("Введите дату брони:")
    await state.set_state(reserve_form.date)


@router.message(reserve_form.date)
async def date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите время брони:")
    await state.set_state(reserve_form.time)


@router.message(reserve_form.time)
async def time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Оставтье комменатарий (либо -):")
    await state.set_state(reserve_form.comment)


@router.message(reserve_form.comment)
async def ps(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await confirm_message(message, state)
    await state.set_state(reserve_form.confirm)


async def confirm_message(message: Message, state: FSMContext):
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
            f"<b>Комментарий</b>: {data['comment']}\n"
        ),
        parse_mode="HTML",
        reply_markup=confirm_kb,
    )


@router.message(F.text == "Подтвердить", reserve_form.confirm)
async def confirm_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data["name"] + " " + data["surname"])
    await message.answer("Спасибо за вашу форму!")
    # db.insert_reserve(
    #     message.from_user.id,
    #     data["name"] + " " + data["surname"],
    #     data["phone"],
    #     data["amount"],
    #     data["date"],
    #     data["time"],
    #     data["comment"],
    # )
    await state.clear()


@router.message(F.text == "Написать кальянному мастеру")
async def send_phone(message: types.Message, state: FSMContext):
    await message.answer(
        """Напиши нам в [Telegram](https://t.me/Cs_Hookah)\nИли в [WhatsApp](https://wa.me/qr/SOVELK6ZAWY3D1)""",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


# @router.message(F.text == "Написать кальянному мастеру")
# async def send_message_to_master(message: Message, state: FSMContext):
#     await message.answer("Напишите сообщения")
#     await state.set_state(reserve_form.name)
