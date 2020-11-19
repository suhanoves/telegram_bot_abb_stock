NOT_FOUND = 'Нет данных'


def info_viewer(product_info: dict):
    strings = list()

    strings.append(f"<b>Серия:</b> {product_info.get('series', NOT_FOUND)}")
    strings.append(f"<b>Артикул:</b> {product_info.get('manufacturer_code', NOT_FOUND)}")
    strings.append(f"<b>Наименование:</b> {product_info.get('product_name', NOT_FOUND)}")
    if product_info['status']:
        strings.append(f"<b>Статус:</b> {product_info['status']['name']}")
    strings.append(f"<b>Страна производства:</b> {product_info.get('country', NOT_FOUND)}")
    strings.append(f"<b>ГЦМ:</b> {product_info.get('price_group', NOT_FOUND)}")
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

    strings.append(f"<b>Скл.статус:</b> {product_info.get('stock_category', NOT_FOUND)}")
    strings.append(f"<b>Срок поставки:</b> {product_info.get('delivery_time', NOT_FOUND)}")

    return '\n'.join(strings)


def size_viwer(producti_info):
    pass


def sctock_viwer(stock_info):
    pass
