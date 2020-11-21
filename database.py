# хранение результатов поиска пользователей
USER_SEARCH_RESULTS = {}
USER_PRODUCT_INFO = {}


def add_user_search_results(user_id: int, search_results: list):
    USER_SEARCH_RESULTS[user_id] = search_results


def del_user_search_history(user_id: int):
    if user_id in USER_SEARCH_RESULTS:
        del USER_SEARCH_RESULTS[user_id]
    if user_id in USER_PRODUCT_INFO:
        del USER_PRODUCT_INFO[user_id]


def get_user_search_results(user_id: int):
    return USER_SEARCH_RESULTS[user_id]


def cash_product_info(user_id: int, product_info: dict):
    USER_PRODUCT_INFO[user_id] = product_info


def get_product_info(user_id: int):
    return USER_PRODUCT_INFO.get(user_id)
