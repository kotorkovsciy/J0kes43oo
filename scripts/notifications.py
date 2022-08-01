from create_bot import bot, notific
from asyncio import sleep


async def scheduled(self):
    while True:
        await sleep(self)
        if await notific.newsJokesExists():
            for i in range(await notific.quantityUsers()):
                row = await notific.newsJoke()
                if row["user_id"] != i+1:
                    userId = await notific.infoId(i+1)
                    await bot.send_message(userId, f"Появилась новая шутка\n\n{row['joke']}\n\nАвтор: {row['author']}")
            await notific.deleteOldJoke()
