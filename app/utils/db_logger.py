import logging

db_logger = logging.getLogger('database')
db_logger.propagate = False
db_logger.setLevel(logging.DEBUG)

db_handler = logging.StreamHandler()
db_handler.setLevel(logging.DEBUG)

db_formatter = logging.Formatter('{asctime} - {name} - {levelname} - {message}', style='{')

db_handler.setFormatter(db_formatter)
db_logger.addHandler(db_handler)
