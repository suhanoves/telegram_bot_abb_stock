from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_search = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Новый запрос')]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
