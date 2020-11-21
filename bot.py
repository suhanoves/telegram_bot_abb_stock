import telebot
import math

import keyboards  # скрипт с клавиатурами
import api_parser  # скрипт backend'а для связи с API
import result_viewer  # скрипт с визуализацией product info
import database

from config import BOT_TOKEN  # скрипт с настройками бота, доступа к API и БД

bot = telebot.TeleBot(f'{BOT_TOKEN}', parse_mode=None)


# TODO удалить после того как восстановят автогенерацию токена
@bot.message_handler(regexp=f"^save_new_token_to_file:")
def save_token(message):
    api_parser.save_token_to_file(message.text[23:])


@bot.message_handler(commands=['start'])
@bot.message_handler(regexp=f"^{keyboards.buttons_text['Новый запрос']}$")
def start_message(message):
    # получаем ID
    user_id = get_user_id(message)

    # удаляем предыдущие результаты поиска по пользователю
    database.del_user_search_history(user_id)

    # выводим стартовое сообщение
    text = 'Всё очень просто: введите <b>артикул</b> или <b>название</b> оборудования и я поищу информацию о нём'

    # удаляем клавиатуру
    keyboard = keyboards.remove_reply_keyboard()

    # отправляем сообщение
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     parse_mode='HTML',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    # читаем файл помощи
    with open('help.html', 'r', encoding='utf-8') as file:
        help_text = file.read()

    # добавляем приветствие пользователя по имени
    greeting = f'Здравствуйте, {message.from_user.first_name}!\n'
    text = greeting + help_text

    # добавляем клавиатуру
    keyboard = keyboards.get_new_search_keyboard()

    # отправляем сообщение
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     parse_mode='HTML',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'manufacturer_code')
@bot.callback_query_handler(func=lambda call: call.data == 'product_name')
def call_search_option(call):
    # получаем telegram IDs
    user_id = get_user_id(call)
    chat_id = get_chat_id(call)
    message_id = get_message_id(call)

    # удаляем инлайн клавиатуру из предыдущего сообщения
    bot.edit_message_reply_markup(chat_id, message_id)

    # забираем артикул/наименование из цитируемого сообщения
    user_query = call.message.reply_to_message.text

    # ищем по артикулу/наименованию получаем список оборудования по запросу
    # нажата кнока по артикулу
    if call.data == 'manufacturer_code':
        search_results = api_parser.get_search_results(manufacturer_code=user_query)
    # нажата кнопка по имени
    else:
        search_results = api_parser.get_search_results(product_name=user_query)

    # если нет результатов поиска
    if not search_results:
        text = 'По вашему запросу ничего не удалось найти. Попробуйте переформулировать текст запроса'
        keyboard = keyboards.remove_reply_keyboard()
        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         reply_markup=keyboard)

    # TODO убрать, как заработает автогенерация токена
    elif search_results == 401:
        print('token просрочен')
        keyboard = keyboards.get_new_search_keyboard()
        bot.send_message(chat_id=chat_id,
                         text='Токен просрочен, сообщите администратору @suhanoves, он починит',
                         reply_markup=keyboard)

    # если результат поиска уникален
    elif len(search_results) == 1:
        # получаем сточку с продуктом
        search_result = get_product_from_search_results(search_results)

        # отправляем сообщение об успешном поискe
        send_success_search_meassage(user_id=user_id,
                                     chat_id=chat_id,
                                     search_result=search_result)

    # если поиск даёт множество совпадений
    else:
        # кешируем результаты поисковой выдачи
        database.add_user_search_results(user_id=user_id,
                                         search_results=search_results)

        # выдаём первую страницу результатов
        text, keyboard = get_search_results_message(search_results=search_results)
        # отправляем сообщение
        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'page' in call.data)
def list_pagination_message(call):
    # получаем ID
    user_id = get_user_id(call)
    chat_id = get_chat_id(call)
    message_id = get_message_id(call)

    # узнаём какую страницу пользователь хочет получить
    current_page = int(call.data.split()[-1])

    # получаем поисковую выдачу по пользователю
    search_results = database.get_user_search_results(user_id)

    text, keyboard = get_search_results_message(search_results=search_results,
                                                current_page=current_page)

    # если сообщение изменилось - меняем текст
    if call.message.text != text:
        # изменяем сообщение с нужной страницей списка
        bot.edit_message_text(text=text,
                              chat_id=chat_id,
                              message_id=message_id,
                              parse_mode='HTML',
                              reply_markup=keyboard)
    else:
        text = f'Вы уже на странице {current_page}'
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=text)


@bot.callback_query_handler(func=lambda call: 'product' in call.data)
def call_product_name(call):
    # получаем ID
    user_id = get_user_id(call)
    chat_id = get_chat_id(call)
    message_id = get_message_id(call)

    # удаляем инлайн клавиатуру из предыдущего сообщения
    bot.edit_message_reply_markup(chat_id, message_id)

    # получаем номер элемента в поисковой выдаче
    product_position = int(call.data.split()[-1]) - 1

    # получаем поисковую выдачу
    search_results = database.get_user_search_results(user_id)

    # получаем информацию о найденном оборудовании
    search_result = get_product_from_search_results(search_results=search_results,
                                                    position=product_position)

    # отправляем сообщение об успешном поиске
    send_success_search_meassage(user_id=user_id,
                                 chat_id=chat_id,
                                 search_result=search_result)


@bot.message_handler(regexp=f"^{keyboards.buttons_text['Информация']}$")
def get_information(message):
    # получаем ID
    user_id = get_user_id(message)
    chat_id = get_chat_id(message)

    # получаем информацию по продукту
    product_info = database.get_product_info(user_id)

    if product_info:
        # получаем форматированный текст сообщения
        text = result_viewer.info_viewer(product_info)

        # добавляем клавиатуру
        keyboard = keyboards.get_info_keyboard()

        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         reply_markup=keyboard)
    else:
        send_empty_search_history_message(chat_id)


@bot.message_handler(regexp=f"^{keyboards.buttons_text['Фотографии']}$")
def get_photo(message):
    # получаем ID
    user_id = get_user_id(message)
    chat_id = get_chat_id(message)

    # получаем информацию по продукту
    product_info = database.get_product_info(user_id)

    if product_info:
        # получаем список ссылок на фотографии
        photos = product_info['photos']

        # добавляем клавиатуру
        keyboard = keyboards.get_info_keyboard()

        if photos:
            for photo in photos:
                bot.send_photo(chat_id=chat_id,
                               photo=photo,
                               reply_markup=keyboard)
        else:
            bot.send_message(chat_id=chat_id,
                             text='Фотографий не обнаружено',
                             reply_markup=keyboard)
    else:
        send_empty_search_history_message(chat_id)


@bot.message_handler(regexp=f"^{keyboards.buttons_text['Сертификаты']}$")
def get_cert(message):
    # получаем ID
    user_id = get_user_id(message)
    chat_id = get_chat_id(message)

    # получаем информацию по продукту
    product_info = database.get_product_info(user_id)

    if product_info:
        # получаем список ссылок на сертификаты
        certificates = product_info['certificates']

        # добавляем клавиатуру
        keyboard = keyboards.get_info_keyboard()

        if certificates:
            for cert in certificates:
                caption = result_viewer.cert_viwer(cert)
                bot.send_document(chat_id=chat_id,
                                  data=cert['url'],
                                  caption=caption,
                                  parse_mode='HTML',
                                  reply_markup=keyboard)
        else:
            bot.send_message(chat_id=chat_id,
                             text='Сертификатов не обнаружено',
                             reply_markup=keyboard)
    else:
        send_empty_search_history_message(chat_id)


@bot.message_handler(regexp=f"^{keyboards.buttons_text['Массогабарит']}$")
def get_dimensions(message):
    # получаем ID
    user_id = get_user_id(message)
    chat_id = get_chat_id(message)

    # получаем информацию по продукту
    product_info = database.get_product_info(user_id)

    if product_info:
        # получаем форматированный текст сообщения
        text = result_viewer.dimensions_viwer(product_info)

        # добавляем клавиатуру
        keyboard = keyboards.get_info_keyboard()

        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         reply_markup=keyboard)
    else:
        send_empty_search_history_message(chat_id)


@bot.message_handler(regexp=f"^{keyboards.buttons_text['Складские остатки']}$")
def get_stock(message):
    # получаем ID
    user_id = get_user_id(message)
    chat_id = get_chat_id(message)

    # получаем информацию по продукту
    product_info = database.get_product_info(user_id)

    if product_info:
        # получаем форматированный текст сообщения
        text = result_viewer.sctock_viwer(product_info)

        # добавляем клавиатуру
        keyboard = keyboards.get_info_keyboard()

        bot.send_message(chat_id=chat_id,
                         text=text,
                         parse_mode='HTML',
                         reply_markup=keyboard)
    else:
        send_empty_search_history_message(chat_id)


@bot.message_handler(func=lambda m: True)
def any_message(message):
    if all(x.isalnum() or x in ' -+=/.,*%' for x in message.text):
        answer = 'Как искать оборудование:\n<b>по артикулу</b> или <b>по названию</b>?'
        keyboard = keyboards.get_search_keyboard()
        bot.reply_to(message=message,
                     text=answer,
                     parse_mode='HTML',
                     reply_markup=keyboard)

    # если в строке есть символы кроме букв и пробелов - заставляем пользователя перефразировать запрос
    else:
        text = 'Запрос содержит недопустимые символы. Перефразируйте запрос'
        bot.send_message(chat_id=message.chat.id,
                         text=text,
                         reply_markup=keyboards.remove_reply_keyboard())


def get_search_results_message(search_results: list, current_page: int = 1):
    # по запросу получаем нужный текст нужной страницы и параметры кнопок для клавиатуры
    text, eqiup_numbers, page_count = list_pagination(search_results=search_results,
                                                      current_page=current_page)
    # генерируем клавиатуру
    keyboard = keyboards.get_pagination_keyboard(eqiup_numbers, current_page, page_count)

    return text, keyboard


def list_pagination(search_results: list, current_page: int = 1):
    # считаем на сколько страниц можно разбить список по 5 элементов
    page_count = math.ceil(len(search_results) / 5)

    # определяем номер первого элемента на странице
    product_start_slice = 5 * (current_page - 1)

    # определяем позицию последнего элемента на странице
    product_end_slice = product_start_slice + 5

    # формируем список строк для печати
    string_of_text = []

    # создаём список нумерации пунктов
    product_numbers = []

    # создаём счётчик нумерации пунктов
    count = product_start_slice

    # наполняем список строками
    for item in search_results[product_start_slice:product_end_slice]:
        count += 1
        product_numbers.append(count)
        # получаем статус оборудования
        status = item['status']
        # получаем название оборудования
        product_name = item['product_name']
        # создаём список пунктов оборудования
        string_of_text.append(f'{count}. <b>{status + "." if status else ""}</b> {product_name} ')
        # увеличиваем счётчик

    # склеиваем пункты списка для формирования сообщения
    text = '\n'.join(string_of_text)

    return text, product_numbers, page_count


def get_product_from_search_results(search_results: list, position: int = 0):
    return search_results[position]


def get_user_id(instance):
    return instance.from_user.id


def get_chat_id(instance):
    if type(instance) == telebot.types.CallbackQuery:
        return instance.message.chat.id
    if type(instance) == telebot.types.Message:
        return instance.chat.id


def get_message_id(instance):
    if type(instance) == telebot.types.CallbackQuery:
        return instance.message.message_id
    if type(instance) == telebot.types.Message:
        return instance.message_id


def send_success_search_meassage(user_id: int, chat_id: int, search_result):
    # получаем информацию по продукту
    product_info = api_parser.get_product_info(search_result['product_id'])

    # кэшируем в базу данных
    database.cash_product_info(user_id=user_id, product_info=product_info)

    # Получаем артикул и название оборудования
    manudacture_code = product_info['manufacturer_code']
    product_name = product_info['product_name']

    # выводим сообщение с клавиатурой с выбором информации по продукту
    string_1 = 'По вашему запросу найдено следующее оборудование:\n'
    string_2 = f"<b>{manudacture_code}</b> {product_name}"
    string_3 = '\nВыберите вид информации, которую вы хотите получить:'
    text = f'{string_1}\n{string_2}\n{string_3}'

    keyboard = keyboards.get_info_keyboard()

    # отправляем сообщение
    bot.send_message(chat_id=chat_id,
                     text=text,
                     parse_mode='HTML',
                     reply_markup=keyboard)


def send_empty_search_history_message(chat_id):
    bot.send_message(chat_id=chat_id,
                     text='История поиска пуста. Выполните новый запрос',
                     reply_markup=keyboards.get_new_search_keyboard())


if __name__ == '__main__':
    print('bot is running')
    bot.infinity_polling()
