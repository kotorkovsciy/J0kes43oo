from create_bot import bot, sql
from asyncio import sleep

sizeQuantity = []


async def quantityUp():
    global sizeQuantity
    krivda = False
    quantity = await sql.quantityJokes()
    sizeQuantity.append(quantity)
    if len(sizeQuantity) > 1:
        if sizeQuantity[-1] > sizeQuantity[-2]:
            krivda = True
        if len(sizeQuantity) > 2:
            del sizeQuantity[0]
    return krivda


async def scheduled(self):
    while True:
        await sleep(self)
        if await quantityUp():
            for i in range(await sql.quantityUsers()):
                row = await sql.newsJoke()
                if row[0] != i+1:
                    userId = await sql.infoId(i+1)
                    await bot.send_message(userId, f"Появилась новая шутка\n\n {row[1]} Автор: {row[2]}")
