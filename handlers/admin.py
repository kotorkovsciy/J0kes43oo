from aiogram import Dispatcher, types
from create_bot import sql
from os import getenv


async def clearc(message: types.Message):
    if int(getenv("ID_ADMIN")) == message.from_user.id:
        await sql.deleteJokes()
        await message.answer('Была произведена очистка')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(clearc, commands=['database_clear'])
