from asyncio import new_event_loop, set_event_loop
from logging import info

from aiogram.utils.executor import start_polling

from create_bot import dp
from handlers import admin, client
from scripts.notifications import scheduled


async def on_startup(_):
    info("Бот вышел в онлайн")

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    loop = new_event_loop()
    set_event_loop(loop)
    loop.create_task(scheduled(60))
    start_polling(dp, skip_updates=True, on_startup=on_startup)
