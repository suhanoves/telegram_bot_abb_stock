from datetime import date

NOT_FOUND = 'Нет данных'
RU_MONTH_VALUES = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}

def info_viewer(product_info: dict):
    strings = list()

    strings.append(f"<b>Серия:</b> {product_info.get('series', NOT_FOUND)}")
    strings.append(f"<b>Артикул:</b> {product_info.get('manufacturer_code', NOT_FOUND)}")
    strings.append(f"<b>Наименование:</b> {product_info.get('product_name', NOT_FOUND)}")
    if product_info['status']:
        strings.append(f"<b>Статус:</b> {product_info['status']['name']}")
    strings.append(f"<b>Страна производства:</b> {product_info.get('country', NOT_FOUND)}")

    price = product_info['price'].get('value', NOT_FOUND)
    currency = product_info['price'].get('currency', '')
    vat = product_info['price'].get('vat', None)
    if vat is None:
        vat = ''
    if vat:
        vat = 'с НДС'
    else:
        vat = 'без НДС'
    strings.append(f"<b>Тариф:</b> {price} {currency}.{vat}")

    strings.append(f"<b>ГЦМ:</b> {product_info.get('price_group', NOT_FOUND)}")
    strings.append(f"<b>Скл.статус:</b> {product_info.get('stock_category', NOT_FOUND)}")
    strings.append(f"<b>Срок поставки:</b> {product_info.get('delivery_time', NOT_FOUND)}")

    return '\n'.join(strings)


def dimensions_viwer(product_info: dict):
    strings = list()
    dimensions = product_info['dimensions']
    pack = product_info['pack']
    params = {'ean': 'Штрих-код:',
              'height': 'Высота:',
              'width': 'Ширина:',
              'depth': 'Глубина:',
              'weight': 'Вес:'}

    strings.append(f'<ins><b>Параметры изделия:</b></ins>')
    for key, value in params.items():
        param = dimensions.get(key, NOT_FOUND)
        param_unit = dimensions.get(f'{key}_unit', '')
        strings.append(f"<b>{value}</b> {param} {param_unit}")

    strings.append('')
    strings.append(f'<ins><b>Параметры упаковки:</b></ins>')
    strings.append(f"<b>Кратность</b>: {pack.get('multiplicity', NOT_FOUND)}")
    for key, value in params.items():
        param = pack.get(key, NOT_FOUND)
        param_unit = pack.get(f'{key}_unit', '')
        strings.append(f"<b>{value}</b> {param} {param_unit}")

    return '\n'.join(strings)


def sctock_viwer(product_info):
    strings = list()
    stocks = product_info['stocks']
    if stocks:
        for stock in stocks:
            strings.append(f"<b>Склад:</b> {stock['stock_name']}")
            strings.append(f"<b>Свободно:</b> {stock['available']} шт.")
            strings.append('')
            strings.append(f"<b>Всего:</b> {stock['in_stock']} шт.")
            strings.append(f"<b>Спрос:</b> {stock['demand']} шт.")
            strings.append(f"<b>Заказано:</b> {stock['ordered']} шт.")
            strings.append(f"<b>В пути:</b> {stock['in_transit']} шт.")
            strings.append(f"<b>Срок поставки:</b> {product_info.get('delivery_time', NOT_FOUND)}")

    else:
        strings.append('Нет информации по складским остаткам')
    return '\n'.join(strings)


def cert_viwer(cert):
    strings = list()

    cert_type = cert.get('type', '')
    strings.append(f"{cert_type}")

    validity_from = cert.get('validity_from', '')
    if validity_from:
        validity_from = date.fromisoformat(validity_from)
        strings.append(f"<b>Действителен от: </b>"
                       f"{validity_from.day} "
                       f"{RU_MONTH_VALUES[validity_from.month]} "
                       f"{validity_from.year}")

    validity_to = cert.get('validity_to', '')
    if validity_to:
        validity_to = date.fromisoformat(validity_to)
        strings.append(f"<b>Действителен до: </b>"
                       f"{validity_to.day} "
                       f"{RU_MONTH_VALUES[validity_to.month]} "
                       f"{validity_to.year}")

        if validity_to < date.today():
            strings.append('<u>Сертификат просрочен!</u>')

    return '\n'.join(strings)
