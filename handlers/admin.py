from aiogram import Dispatcher, types
from create_bot import sql


async def clearc(message: types.Message):
    await sql.delete_jokes()
    await message.answer('Была произведена очистка')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(clearc, commands=['clearclearclearclrcls'])
