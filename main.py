import asyncio
import logging

from aiogram.utils import executor

from create_bot import dp
from handlers import admin, client, other
from scripts.notifications import scheduled


async def on_startup(_):
  logging.info("Бот вышел в онлайн")

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.create_task(scheduled(60))
  executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
