import os
import dotenv

dotenv.load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DB_NAME = os.getenv('DB_NAME')
SHELVE_NAME = os.getenv('SHELVE_NAME')
