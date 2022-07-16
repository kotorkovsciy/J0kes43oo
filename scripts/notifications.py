from create_bot import bot, sql
from asyncio import sleep


async def scheduled(self):
    while True:
        await sleep(self)
        if await sql.newsJokesExists():
            for i in range(await sql.quantityUsers()):
                row = await sql.newsJoke()
                if row[0] != i+1:
                    userId = await sql.infoId(i+1)
                    await bot.send_message(userId, f"Появилась новая шутка\n\n{row[1]}\n\nАвтор: {row[2]}")
            await sql.deleteOldJoke()
