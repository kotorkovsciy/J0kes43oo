from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import logging
from scripts.sql_data import Database
import os

from dotenv import load_dotenv

load_dotenv()

sql = Database('joke.db')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)