from os import getenv

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN = int(getenv('ADMIN'))
