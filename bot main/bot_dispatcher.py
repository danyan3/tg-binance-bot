from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN_BOT')

allowed_users = [
    364372563, # Ya
    1369199498, # Zakashcik
    678377836, # Nikita
]

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())