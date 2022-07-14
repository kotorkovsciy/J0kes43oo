from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from logging import basicConfig, INFO
from scripts import Database, getAnekdot
from os import getenv
from dotenv import load_dotenv

load_dotenv()

sql = Database('jokes.db')
Anekdot = getAnekdot()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
basicConfig(level=INFO)
