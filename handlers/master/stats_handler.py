from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state_list import item, expenses
from db import DataBase
from all_kb import (
    STATS,
    ITEMS_TODAY,
    BACK,
    SEE_INCOME,
    OPEN,
    GET_MONTH_SALARY,
    master_kb,
    stats_kb,
)

router = Router()

db = DataBase()

@router.message(F.text == STATS)
async def stats(message: Message, state: FSMContext):
    await message.answer("Ага", reply_markup=stats_kb)


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

@router.message(F.text == ITEMS_TODAY)
async def items_today(message: Message, state: FSMContext):
    data = await state.get_data()
    if "duty_id" in data:
        items = db.get_items_today(data["duty_id"])
        res = [f"{name} -- {price} -- {comment}" for name, price, comment in items]
        await message.answer(f"Продажи: \n {"\n".join(res)}")
    else:
        await message.answer("Смена не твоя вроде")


@router.message(F.text == OPEN)
async def open_duty(message: Message, state: FSMContext):
    duty = db.get_active_duty()
    master_id = db.get_hookah_master(message.from_user.id)

    if duty is not None and duty[1] == master_id:
        await state.update_data(master_id=master_id, duty_id=duty[0])
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
    if len(data) > 0:
        res = [f"{name}: {salary}" for name, salary in data]
        await message.answer(
            f"""Зарплата за месяц:\n{"\n".join(res)}"""
        )
    else:
        await message.answer(
            """Пока нечего считать"""
        )
