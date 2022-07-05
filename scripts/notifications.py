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
                user_id = await sql.infoId(id)
                user_id = str(tuple(user_id))
                user_id = sub(r"[^0-9]+", '', user_id)
                user_id = int(user_id)
                await bot.send_message(user_id, "Появилась новая шутка")
