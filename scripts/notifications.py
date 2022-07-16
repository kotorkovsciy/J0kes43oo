from create_bot import bot, sql
from asyncio import sleep


async def scheduled(self):
    while True:
        await sleep(self)
        if await sql.newsJokesExists():
            for i in range(await sql.quantityUsers()):
                row = await sql.newsJoke()
                if row["user_id"] == i+1:
                    userId = await sql.infoId(i+1)
                    await bot.send_message(userId, f"Появилась новая шутка\n\n{row['joke']}\n\nАвтор: {row['author']}")
            await sql.deleteOldJoke()
