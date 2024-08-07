# from datetime import datetime
# from aiogram_datepicker import Datepicker, DatepickerSettings
# from aiogram.types import Message, CallbackQuery
# from aiogram import F, Router


# # router= Router()

# def _get_datepicker_settings():
#     return DatepickerSettings() #some settings

# # @router.message_handler(state='*')
# # async def _main(message: Message):
# #     datepicker = Datepicker(_get_datepicker_settings())

# #     markup = datepicker.start_calendar()
# #     await message.answer('Select a date: ', reply_markup=markup)
    
# # @router.callback_query_handler(Datepicker.datepicker_callback.filter())
# # async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
# #     datepicker = Datepicker(_get_datepicker_settings())

# #     date = await datepicker.process(callback_query, callback_data)
# #     if date:
# #         await callback_query.message.answer(date.strftime('%d/%m/%Y'))

# #     await callback_query.answer()


# DatepickerSettings(
#     initial_view='day',  #available views -> day, month, year
#     initial_date=datetime.now().date(),  #default date
#     views={
#         'day': {
#             'show_weekdays': True,
#             'header': ['prev-year', 'days-title', 'next-year'],
#             'footer': ['prev-month', 'select', 'next-month'], #if you don't need select action, you can remove it and the date will return automatically without waiting for the button select
#             #available actions -> prev-year, days-title, next-year, prev-month, select, next-month, ignore
#         },
#         'month': {
#             'months_labels': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Нов', 'Дек'],
#             'header': [
#                         'prev-year', 
#                         ['year', 'select'], #you can separate buttons into groups
#                         'next-year'
#                        ], 
#             'footer': ['select'],
#             #available actions -> prev-year, year, next-year, select, ignore
#         },
#         # 'year': {
#         #     'header': [],
#         #     'footer': [],
#         #     #available actions -> prev-years, ignore, next-years
#         # }
#     },
#     labels={
#         'prev-year': '<<',
#         'next-year': '>>',
#         'prev-years': '<<',
#         'next-years': '>>',
#         'days-title': '{month} {year}',
#         'selected-day': '{day} *',
#         'selected-month': '{month} *',
#         'present-day': '• {day} •',
#         'prev-month': '<',
#         'select': 'Select',
#         'next-month': '>',
#         'ignore': ''
#     },
#     custom_actions=[] #some custom actions
# )