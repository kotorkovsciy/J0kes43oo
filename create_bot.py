from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from logging import basicConfig, INFO
from scripts import Database, getAnekdot, AdminDatabase, NotificationsDatabase, JokesDatabase
from os import getenv
from dotenv import load_dotenv

load_dotenv()

Anekdot = getAnekdot()
sql = Database('jokes')
adm_sql = AdminDatabase('jokes')
notific = NotificationsDatabase('jokes')
jokes = JokesDatabase('jokes')

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
basicConfig(level=INFO)
