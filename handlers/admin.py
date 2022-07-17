from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from create_bot import sql
from os import getenv, remove
from keyboards import kb_admin


async def cmd_start_adm(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Вы в админской", reply_markup=kb_admin)


async def clear_database(message: types.Message):
    if message.chat.type == 'private':
        if int(getenv("ID_ADMIN")) == message.from_user.id:
            await sql.deleteJokes()
            await message.answer('Была произведена очистка')


async def sql_damp(message: types.Message):
    if message.chat.type == 'private':
        if int(getenv("ID_ADMIN")) == message.from_user.id:
            await sql.dump(message.from_user.id)
            file = open(f"{message.from_user.id}.sql", 'rb')
            await message.answer_document(file, caption="sql dump")
            remove(f"{message.from_user.id}.sql")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_start_adm, commands="start_adm")
    dp.register_message_handler(clear_database, Text(
        equals="Очистка бд"))
    dp.register_message_handler(sql_damp, Text(
        equals="Дамп бд"))
