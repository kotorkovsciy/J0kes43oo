from re import sub
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import sql
from keyboards import kb_client, kb_record
from scripts import getanekdot


class record(StatesGroup):
    joke = State()
    author = State()


async def cmd_start(message: types.Message):
    if message.chat.type == 'private':
        if not await sql.userExists(message.from_user.id):
            await sql.userAdd(message.from_user.id)
    await message.answer("Что выбираете ?", reply_markup=kb_client)


async def bot_joke(message: types.Message):
    try:
        await message.reply(await sql.randomJoke())
    except:
        await message.reply('Шуток нету')


async def random_joke(message: types.Message):
    msg = await message.answer("Загружаю")
    msg1 = await msg.edit_text(getanekdot())


async def my_joke(message: types.Message):
    try:
        await message.answer(await sql.myJoke(message.from_user.id))
    except:
        await message.answer("Нету ваших шуток")


async def delet_joke(message: types.Message):
    await sql.deleteJokesUser(message.from_user.id)
    await message.answer("Шутки удалены")


async def joke_step(message: types.Message, state: FSMContext):
    global quantity
    await message.answer(text='Напиши шутку', reply_markup=kb_record)
    quantity = await sql.quantityJokesUser(message.from_user.id)
    quantity = str(tuple(quantity))
    quantity = sub(r"[^0-9]+", '', quantity)
    quantity = int(quantity)
    if quantity < 10:
        await record.joke.set()
    else:
        await state.finish()
        await message.answer(f'Превышен лимит шуток {quantity}/10', reply_markup=kb_client)


async def author_step(message: types.Message, state: FSMContext):
    await state.update_data(joke=message.text)
    await message.answer(text='Введите автора')
    await record.author.set()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=kb_client)


async def res_step(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    user_data = await state.get_data()
    await sql.recordJoke(user_data['joke'], user_data['author'], message.from_user.id)
    await message.answer(f"Записано {quantity+1}/10", reply_markup=kb_client)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(bot_joke, Text(
        equals="Шутку пользователей бота"))
    dp.register_message_handler(
        random_joke, lambda message: message.text == "Шутку рандомную из инета")
    dp.register_message_handler(
        my_joke, lambda message: message.text == "Мои шутки")
    dp.register_message_handler(
        delet_joke, lambda message: message.text == "Удалить мои Шутки")
    dp.register_message_handler(
        joke_step, lambda message: message.text == "Записать шутку", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(
        equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(
        author_step, state=record.joke, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        res_step, state=record.author, content_types=types.ContentTypes.TEXT)
