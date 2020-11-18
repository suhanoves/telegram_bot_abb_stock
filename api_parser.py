import config
import requests

def generate_new_token(session):
    """Generate a new token for API and save it to the file 'token.txt'
    Token lifetime is 10 hours"""

    # headers with auth data for request
    auth_data = {
        'email': config.LOGIN,
        'password': config.PASSWORD
    }

    auth_response = session.post(config.AUTH_URL, json=auth_data)
    token = auth_response.json()['token']

    with open('token', 'w', encoding='utf-8') as file:
        file.write(token)


def get_token():
    with open('token', 'r', encoding='utf-8') as file:
        return file.read()


def get_session():
    token = get_token()

    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}'})
    return session


def get_search_results(manufacturer_code: str = '', product_name: str = ''):
    """
    Get a list of equipment by product_id or product name
    manufacturerCode - Product ID, like '2CDS253001R0164'
    name             - Extended Product Type, like 'S203 C16'
    perPage          - the number of lines in the list
    """

    session = get_session()
    params = {'manufacturerCode': manufacturer_code,
              'name': product_name,
              'sort': 'manufacturerCode',
              }

    search_results = session.get(config.API_URL, params=params)

    return search_results


def get_product_info(product_id: str):
    session = get_session()

    raw_info = session.get(f'{config.API_URL}products/{product_id}').json()

    prices = session.get(f'{config.API_URL}products/{product_id}/prices').json()
    raw_info['prices'] = prices

    stocks = session.get(f'{config.API_URL}products/{product_id}/remains').json()
    raw_info['stocks'] = stocks

    photos = session.get(f'{config.API_URL}/gallery/{product_id}').json()
    raw_info['photos'] = photos

    prodict_info = formated_product_info(raw_info)

    # TODO убрать логирование
    with open('json/product/general_info.json', 'w', encoding='utf-8') as file:
        json.dump(prodict_info, file, ensure_ascii=False, indent=4)

    return prodict_info


def formated_product_info(raw_info: dict):
    product_info = dict()

    product_info['manufacturer_code'] = raw_info['manufacturerCode']
    product_info['name'] = raw_info['names']['ru']
    product_info['status'] = raw_info['status']
    product_info['series'] = raw_info['additionalFields']['marketingSeries']
    product_info['country'] = raw_info['additionalFields']['country']
    product_info['delivery_time'] = raw_info['additionalFields']['deliveryDate']
    product_info['price_group'] = raw_info['additionalFields']['priceGroup']
    product_info['stock_category'] = raw_info['additionalFields']['stock']

    # get prices
    try:
        product_info['price'] = dict()
        price = raw_info.get('prices')[0]
        product_info['price']['value'] = price['value']
        product_info['price']['currency'] = price['currency']['sign']
    except IndexError:
        product_info['price'] = {}

    # get product dimensions
    product_info['dimensions'] = {}
    product_info['dimensions']['ean'] = raw_info.get('additionalFields').get('ean')

    dimensions = raw_info.get('sizeCharacteristics')
    product_info['dimensions']['height'] = dimensions['height']
    product_info['dimensions']['height_unit'] = dimensions['heightUnit']['conventNationalView']
    product_info['dimensions']['width'] = dimensions['width']
    product_info['dimensions']['width_unit'] = dimensions['widthUnit']['conventNationalView']
    product_info['dimensions']['depth'] = dimensions['depth']
    product_info['dimensions']['depth_unit'] = dimensions['depthUnit']['conventNationalView']

    # get pack dimentions
    try:
        product_info['pack'] = {}
        pack = raw_info.get('packs')[0]

        product_info['pack']['multiplicity'] = pack['multiplicity']
        product_info['pack']['ean'] = pack['ean']

        product_info['pack']['height'] = pack['height']
        product_info['pack']['height_unit'] = pack['heightUnit']['conventNationalView']
        product_info['pack']['width'] = pack['width']
        product_info['pack']['width_unit'] = pack['widthUnit']['conventNationalView']
        product_info['pack']['depth'] = pack['depth']
        product_info['pack']['depth_unit'] = pack['depthUnit']['conventNationalView']

        product_info['pack']['weight'] = pack['weight']
        product_info['pack']['weight_unit'] = pack['weightUnit']['conventNationalView']
    except IndexError:
        product_info['pack'] = {}

    # get stock balance
    stocks = []
    for stock in raw_info['stocks']:
        current_stock = dict()
        current_stock['stock_name'] = stock['stock']['name']
        current_stock['available'] = stock['value']
        current_stock['in_stock'] = stock['additionalFields']['totalCount']
        current_stock['demand'] = stock['additionalFields']['demand']
        current_stock['ordered'] = stock['additionalFields']['ordered']
        current_stock['in_transit'] = stock['additionalFields']['inTransit']

        stocks.append(current_stock)
    product_info['stocks'] = stocks

    # get certificates
    certificates = []
    for cert in raw_info['additionalFields']['certificates']:
        current_cert = dict()
        current_cert['type'] = cert['type']
        current_cert['cert'] = config.CERT_URL + cert['filePath']
        current_cert['validity_from'] = cert['validityPeriodFrom']
        current_cert['validity_to'] = cert['validityPeriodTo']
        certificates.append(current_cert)
    product_info['certificates'] = certificates

    # get photo gallery
    try:
        photos = raw_info.get('photos')
        product_info['photos'] = [config.GALLERY_URL + photo['mdmUrl'] for photo in photos]
    except IndexError:
        product_info['photos'] = raw_info.get('images').get('max')

    return product_info