from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

product_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ℹ Информация'),
            KeyboardButton(text='📷 Фотографии')
        ],
        [
            KeyboardButton(text='📄 Сертификаты'),
            KeyboardButton(text='📦 Массогабарит')
        ],
        [
            KeyboardButton(text='🚚 Складские остатки')
        ],
        [
            KeyboardButton(text='🔎 Новый запрос')
        ]
    ],
    resize_keyboard=True,
)
