from create_bot import bot, sql
from asyncio import sleep


async def scheduled(self):
    while True:
        await sleep(self)
        if await sql.oldQuantityJokes() < await sql.quantityJokes():
            await sql.recordQuantityJokes()
            for i in range(await sql.quantityUsers()):
                row = await sql.newsJoke()
                if row[0] != i+1:
                    userId = await sql.infoId(i+1)
                    await bot.send_message(userId, f"Появилась новая шутка\n\n {row[1]} Автор: {row[2]}")
