from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from state_list import reserve_form
from all_kb import confirm_kb, start_kb,  get_phone_kb
from db import DataBase

# from aiogram_datepicker import Datepicker, DatepickerSettings
# from handlers.calendar.common import _get_datepicker_settings

router = Router()

db = DataBase()


@router.message(F.text == "Забронировать столик")
async def form(message: Message, state: FSMContext):
    data = db.get_user_id(message.from_user.id)
    if data is not None:
        await state.update_data(data=data)
        await message.answer("Введите кол-во человек:")
        await state.set_state(reserve_form.amount)
    else:
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
    # datepicker = Datepicker(_get_datepicker_settings())

    # markup = datepicker.start_calendar()
    # await message.answer('Select a date: ', reply_markup=markup)
    await message.answer("Введите дату брони:")
    await state.set_state(reserve_form.date)

# @router.callback_query(Datepicker.datepicker_callback.filter())
# async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
#     datepicker = Datepicker(_get_datepicker_settings())

#     date = await datepicker.process(callback_query, callback_data)
#     if date:
#         await callback_query.message.answer(date.strftime('%d/%m/%Y'))

#     await callback_query.answer()


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
            f"Данные по бронированию:\n"
            f"<b>Имя</b>: {data['name']}\n"
            f"<b>Фамилия</b>: {data['surname']}\n"
            f"<b>Телефон для связи</b>: {data['phone']}\n"
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
