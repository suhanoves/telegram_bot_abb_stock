def info_viewer(product_info):
    strings = []

    if product_info.get('additionalFields').get('marketingSeries'):
        strings.append(f"<b>Серия:</b> {product_info['additionalFields']['marketingSeries']}")
    if product_info.get('manufacturerCode'):
        strings.append(f"<b>Артикул:</b> {product_info['manufacturerCode']}")

    if product_info.get('descriptions').get('ru'):
        strings.append(f"<b>Наименование:</b> {product_info['descriptions']['ru']}")
    elif product_info.get('names').get('ru'):
        strings.append(f"<b>Наименование:</b> {product_info['names']['ru']}")

    strings.append('')
    if product_info.get('status'):
        strings.append(f"<b>Статус:</b> {product_info['status']}")

    if product_info.get('additionalFields').get('country'):
        strings.append(f"<b>Страна производства:</b> {product_info['additionalFields']['country']}")

    strings.append('')
    if product_info.get('price'):
        strings.append(f"<b>Тариф:</b> {product_info['price']} руб.БЕЗ НДС")

    if product_info.get('additionalFields').get('priceGroup'):
        strings.append(f"<b>ГЦМ:</b> {product_info['additionalFields']['priceGroup']}")
    if product_info.get('additionalFields').get('stock'):
        strings.append(f"<b>Скл.статус:</b> {product_info['additionalFields']['stock']}")

    if product_info.get('additionalFields').get('deliveryDate'):
        strings.append(f"<b>Срок поставки:</b> {product_info['additionalFields']['deliveryDate']}")
    if product_info.get('packs').[0].get('deliveryDate'):
        strings.append(f"<b>Кратность:</b> {product_info['packs'][0]['multiplicity']}")

    return '\n'.join(strings)


def photo_viewer(product_info):
    return [product_info.get('images').get('max')]


def cert_viewer(product_info):
    pass


def size_viwer(producti_info):
    pass


def sctock_viwer(stock_info):
    pass
