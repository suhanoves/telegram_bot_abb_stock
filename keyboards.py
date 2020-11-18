from telebot import types
from keyboard_paginator import InlineKeyboardPaginator

# создаём список отображений всех кнопок бота
buttons_text = {'Новый запрос': '🔎 Новый запрос',
                'Информация': 'ℹ Информация',
                'Фотографии': '📷 Фотографии',
                'Сертификаты': '📄 Сертификаты',
                'Массогабарит': '📦 Массогабарит',
                'Складские остатки': '🚚 Складские остатки',
                }

# создаём список экземпляров класса кнопка чтобы добавлять их в клавиатуры
buttons = {name: types.KeyboardButton(view) for name, view in buttons_text.items()}


def get_find_keyboard():
    # инициализируем клавиатуру с кнопками внутри чата
    find_keyboard = types.InlineKeyboardMarkup(row_width=2)
    # инициализируем кнопки
    button1 = types.InlineKeyboardButton(text='По артикулу', callback_data='manufacturer_code')
    button2 = types.InlineKeyboardButton(text='По названию', callback_data='product_name')
    # Добавляем кнопки на экран
    find_keyboard.add(button1, button2)
    # возвращаем клавиатуру
    return find_keyboard


def get_help_keyboard():
    # создаём клавиатуру
    help_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # добавляем кнопку в клавиатуру
    help_keyboard.add(buttons['Новый запрос'])
    # возвращаем клавиатуру
    return help_keyboard


def get_info_keyboard():
    # создаём клавиатуру
    info_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # группируем кнопки в ряды и добавляем на клавиатуру
    info_keyboard.row(buttons['Информация'], buttons['Фотографии'])
    info_keyboard.row(buttons['Сертификаты'], buttons['Массогабарит'])
    info_keyboard.row(buttons['Складские остатки'])
    info_keyboard.row(buttons['Новый запрос'])
    # возвращаем клавиатуру
    return info_keyboard


def get_list_choice_keyboard():
    # Инициализируем клавиатуру с кнопками внутри чата
    inline_keyboard = types.InlineKeyboardMarkup()

    # По очереди готовим текст и обработчик для каждого знака зодиака
    chat_button1 = types.InlineKeyboardButton(
        text='Контактор AF16-30-10-11 с универсальной катушкой управления 24-60B AC / 20-60B DC',
        callback_data='choice')
    chat_button2 = types.InlineKeyboardButton(
        text='Контактор AF16-30-01-11 с универсальной катушкой управления 24-60B AC / 20-60B DC',
        callback_data='choice')

    # И добавляем кнопку на экран
    inline_keyboard.add(chat_button1)
    inline_keyboard.add(chat_button2)

    return inline_keyboard


def get_pagination_keyboard(product_numbers: list, current_page: int, page_count: int):
    # создаём кнопки пагинации
    paginator = InlineKeyboardPaginator(
        page_count,
        current_page=current_page,
        data_pattern='page {page}')

    # создаём список для кнопок выбора оборудования
    product_buttons = []

    # добавляем названия кнопкок в формате [(text, callback_data),]
    for number in product_numbers:
        product_buttons.append(types.InlineKeyboardButton(text=f'{number}', callback_data=f'product {number}'))

    # добавляем кнопки с выбором оборудования
    paginator.add_before(*product_buttons)

    return paginator.markup


def remove_reply_keyboard():
    return types.ReplyKeyboardRemove()
