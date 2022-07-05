from create_bot import bot, sql
from re import sub
from asyncio import sleep

sizeQuantity = []


async def quantityUp():
    global sizeQuantity
    krivda = False
    quantity = await sql.quantityJokes()
    quantity = str(tuple(quantity))
    quantity = sub(r"[^0-9]+", '', quantity)
    quantity = int(quantity)
    sizeQuantity.append(quantity)
    if len(sizeQuantity) > 1:
        if sizeQuantity[-1] > sizeQuantity[-2]:
            krivda = True
        if len(sizeQuantity) > 2:
            del sizeQuantity[0]
    return krivda


async def quantityUsers():
    quantity = await sql.quantityUsers()
    quantity = str(tuple(quantity))
    quantity = sub(r"[^0-9]+", '', quantity)
    quantity = int(quantity)
    return quantity


async def scheduled(self):
    while True:
        id = 0
        await sleep(self)
        if await quantityUp():
            while await quantityUsers() > id:
                id += 1
                userId = await sql.infoId(id)
                userId = str(tuple(userId))
                userId = sub(r"[^0-9]+", '', userId)
                userId = int(userId)
                await bot.send_message(userId, "Появилась новая шутка")
