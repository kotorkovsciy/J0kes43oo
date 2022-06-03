from aiogram import Dispatcher, types
from create_bot import dp


async def echo_send(message: types.Message):
    pass

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
