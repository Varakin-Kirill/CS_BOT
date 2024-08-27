from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state_list import item
from db import DataBase
from all_kb import (
    SELL,
    SEE_SALARY,
    SEE_INCOME,
    OPEN,
    GET_MONTH_SALARY,
    select_item_markup,
    select_item_buttons,
    ItemCallback,
    PaymentCallback,
    master_kb,
    payment_kb,
)
from aiogram.filters import Command

router = Router()

db = DataBase()


@router.message(F.text == SELL)
async def select_item(message: Message, state: FSMContext):
    duty = db.get_active_duty()
    if duty[2] == message.from_user.id:
        buttons = select_item_buttons()
        markup = select_item_markup(buttons)
        await state.set_state(item.apply)
        await message.answer("Обоснуй че продал", reply_markup=markup)
    else:
        await message.answer("Не твоя смена")


@router.callback_query(ItemCallback.filter(), item.apply)
async def apply_item(
    query: CallbackQuery, state: FSMContext, callback_data: ItemCallback
):
    await state.update_data(item_id=callback_data.item_id)
    await state.set_state(item.payment)
    await query.message.answer("Какая оплата", reply_markup=payment_kb)


@router.callback_query(PaymentCallback.filter(), item.payment)
async def comment_item(
    query: CallbackQuery, state: FSMContext, callback_data: PaymentCallback
):
    await state.update_data(payment=callback_data.payment_type)
    await state.set_state(item.comment)
    await query.message.answer("Добавишь коммент?")


@router.message(item.comment)
async def confirm_item(message: Message, state: FSMContext):
    data = await state.get_data()
    db.insert_buy(data["item_id"], data["master_id"], data["payment"], message.text)
    await state.set_state(None)
    await state.update_data(item_id=None)
    await state.update_data(payment=None)
    await message.answer("Имей сто рублей")


@router.message(F.text == SEE_INCOME)
async def see_day_income(message: Message, state: FSMContext):
    data = await state.get_data()
    if "duty_id" in data:
        hookahs = db.get_master_data(data["master_id"], data["duty_id"])
        if hookahs is not None:
            salary = hookahs[0] - 1000 + 1250 if hookahs[1] > 10 else 1250
            await message.answer(f"Кароче: Каликов {hookahs[1]}, заработал: {salary}")
        else:
            await message.answer("Походу нихуя не было еще")
    else:
        await message.answer("Смена не твоя вроде")


@router.message(F.text == OPEN)
async def open_duty(message: Message, state: FSMContext):
    duty = db.get_active_duty()
    master_id = db.get_hookah_master(message.from_user.id)

    if duty is not None and duty[1] == master_id:
        await message.answer("Ты нахуя дважды смену открываешь додик")
    # elif duty is not None and duty[1] != data["master_id"]:
    #     await message.answer("Додик не закрыл предыдущую смену, так что иди нахуй")
    else:
        try:
            db.open_duty(master_id)
            id = db.get_active_duty()
            await state.update_data(master_id=master_id, duty_id=id[0])
            await message.answer("Удачной смены нахуй", reply_markup=master_kb)
        except Exception as error:
            print("An exception occurred:", error)
            await message.answer("А ты че нахуй, не твоя смена, съебал отсюда")


@router.message(F.text == GET_MONTH_SALARY)
async def get_month_salary(message: Message):
    data = db.get_month_salary()
    print(data)
    await message.answer(
        f"""Зарплата за месяц:\n{data[0][0]}:{data[0][1]}\n{data[1][0]}:{data[1][1]}"""
    )


# @router.message(F.text == CLOSE)
# async def see_day_income(message: Message, state : FSMContext):
#     data = await state.get_data()
#     try:
#         db.close_duty(data["master_id"], data["duty_id"])
#         await message.answer("пиздуй отдыхать")
#     except Exception as error:
#         print("An exception occurred:", error)
#         await message.answer("Даже думать не хочу че пошло не так, но ты обосрался")
