from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from logging import basicConfig, INFO
from scripts import Database, getAnekdot, AdminDatabase
from asyncio import run
from os import getenv
from dotenv import load_dotenv

load_dotenv()

Anekdot = run(getAnekdot())
sql = run(Database('jokes.db'))
adm_sql = run(AdminDatabase('jokes.db'))

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
basicConfig(level=INFO)
