import config
import requests


def generate_new_token():
    """Generate a new token for API and save it to the file 'token.txt'
    Token lifetime is 10 hours"""

    # headers with auth data for request
    auth_data = {
        'email': config.LOGIN,
        'password': config.PASSWORD
    }

    # send a request for generate new token by the server
    auth_response = requests.post(config.AUTH_URL, json=auth_data)

    # get token from json
    token = auth_response.json()['token']

    save_token_to_file(token)


def save_token_to_file(token):
    # save token to the file
    with open('token', 'w', encoding='utf-8') as file:
        file.write(token)


def get_token():
    # get token by read the file
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
              'sort': 'manufacturerCode'
              }
    response = session.get(f"{config.API_SEARCH_URL}", params=params)

    # if status OK or similar
    if response:
        search_results = response.json()
        formated_results = format_search_results(search_results)
        return formated_results
    # if status "Unauthorized"
    elif response.status_code == 401:
        # TODO расскоментировать, когда восстановят автогенерацию токена
        # generate_new_token()
        # get_session()
        # get_search_results(manufacturer_code=manufacturer_code, product_name=product_name)
        return response.status_code


def get_product_info(product_id: str):
    session = get_session()

    raw_info = session.get(f'{config.API_SEARCH_URL}/{product_id}').json()

    prices = session.get(f'{config.API_SEARCH_URL}/{product_id}/prices').json()
    raw_info['prices'] = prices

    stocks = session.get(f'{config.API_SEARCH_URL}/{product_id}/remains').json()
    raw_info['stocks'] = stocks

    photos = session.get(f'{config.API_URL}/gallery/{product_id}').json()
    raw_info['photos'] = photos

    prodict_info = format_product_info(raw_info)

    return prodict_info


def format_search_results(raw_results: dict):
    list_of_results = raw_results['items']

    formated_results = []
    bad_statuses = ('Inactive',
                    'Не используется',
                    'Нужен номер партии',
                    'Obsolete (Phase Out)')

    for result in list_of_results:
        status = result['status']['name'] if result['status'] else None
        current_result = dict(product_id=result['id'],
                              manufacturer_code=result['manufacturerCode'],
                              product_name=result['names']['ru'],
                              status=status)
        if status not in bad_statuses:
            formated_results.append(current_result)

    return formated_results


def format_product_info(raw_info: dict):
    product_info = dict()
    product_info['manufacturer_code'] = raw_info['manufacturerCode']
    product_info['product_name'] = raw_info['names']['ru']
    product_info['status'] = raw_info['status']['name'] if product_info.get('status') else None
    product_info['series'] = raw_info['additionalFields'].get('marketingSeries')
    product_info['country'] = raw_info['additionalFields'].get('country')
    product_info['delivery_time'] = raw_info['additionalFields'].get('deliveryDate')
    product_info['price_group'] = raw_info['additionalFields'].get('priceGroup')
    product_info['stock_category'] = raw_info['additionalFields'].get('stock')

    # get prices
    try:
        product_info['price'] = dict()
        price = raw_info.get('prices')[0]
        product_info['price']['value'] = price['value']
        product_info['price']['currency'] = price['currency']['sign']
        product_info['price']['vat'] = price['withVat']
    except IndexError:
        product_info['price'] = {}

    # get product dimensions
    product_info['dimensions'] = {}
    product_info['dimensions']['ean'] = raw_info.get('additionalFields').get('ean')

    dimensions = raw_info.get('sizeCharacteristics')
    if dimensions:
        product_info['dimensions']['height'] = dimensions['height']
        product_info['dimensions']['height_unit'] = dimensions['heightUnit']['conventNationalView']
        product_info['dimensions']['width'] = dimensions['width']
        product_info['dimensions']['width_unit'] = dimensions['widthUnit']['conventNationalView']
        product_info['dimensions']['depth'] = dimensions['depth']
        product_info['dimensions']['depth_unit'] = dimensions['depthUnit']['conventNationalView']

        product_info['dimensions']['weight'] = dimensions['weight']
        product_info['dimensions']['weight_unit'] = dimensions['weightUnit']['conventNationalView']
    else:
        product_info['dimensions'] = None

    # get pack dimensions
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
    if raw_info.get('stocks'):
        for stock in raw_info['stocks']:
            current_stock = dict()
            current_stock['stock_name'] = stock['stock']['name']
            current_stock['available'] = round(stock['value'])
            current_stock['in_stock'] = round(stock['additionalFields']['totalCount'])
            current_stock['demand'] = round(stock['additionalFields']['demand'])
            current_stock['ordered'] = round(stock['additionalFields']['ordered'])
            current_stock['in_transit'] = round(stock['additionalFields']['inTransit'])

            stocks.append(current_stock)
    product_info['stocks'] = stocks

    # get certificates
    certificates = []
    if raw_info['additionalFields'].get('certificates'):
        for cert in raw_info['additionalFields']['certificates']:
            current_cert = dict()
            current_cert['type'] = cert['type']

            current_cert['url'] = f"{config.CERT_URL}/{cert['filePath']}"
            current_cert['validity_from'] = cert['validityPeriodFrom']
            current_cert['validity_to'] = cert['validityPeriodTo']
            certificates.append(current_cert)
    product_info['certificates'] = certificates

    # get photo gallery
    try:
        photos = raw_info.get('photos')
        product_info['photos'] = [f"{config.GALLERY_URL}/{photo['mdmUrl']}" for photo in photos]
    except IndexError:
        product_info['photos'] = raw_info.get('images').get('max')

    return product_info
