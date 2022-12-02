from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import sql, Anekdot, jokes
from keyboards import kb_client, kb_record, kb_aon


class ClientRecord(StatesGroup):
    quantity = State()
    joke = State()
    author = State()


class ClientDelete(StatesGroup):
    user_id = State()
    aon = State()


async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        await sql.userExists(message.from_user.id)
    await message.answer("Что выбираете ?", reply_markup=kb_client)


async def random_bot_joke(message: types.Message):
    await message.reply(await jokes.randomJoke())


async def random_joke(message: types.Message):
    msg = await message.answer("Загружаю")
    await msg.edit_text(await Anekdot.getAnekdot())


async def my_joke(message: types.Message):
    await message.answer(await jokes.myJoke(message.from_user.id))


async def delet_step(message: types.Message, state: FSMContext):
    await ClientDelete.user_id.set()
    await state.update_data(user_id=message.from_user.id)
    await message.answer("Вы уверены ?", reply_markup=kb_aon)
    await ClientDelete.aon.set()


async def delete_res(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await jokes.deleteJokesUser(user_data["user_id"])
    await state.finish()
    await message.answer("🗑 Шутки удалены 🗑", reply_markup=kb_client)


async def joke_step(message: types.Message, state: FSMContext):
    await ClientRecord.quantity.set()
    quantity = await jokes.quantityJokesUser(message.from_user.id)
    await state.update_data(quantity=quantity)
    if quantity < 10:
        await message.answer("Напиши шутку", reply_markup=kb_record)
        await ClientRecord.joke.set()
    else:
        await state.finish()
        await message.answer(
            f"Превышен лимит шуток {quantity}/10", reply_markup=kb_client
        )


async def author_step(message: types.Message, state: FSMContext):
    await state.update_data(joke=message.text)
    await message.answer("Введите автора", reply_markup=kb_record)
    await ClientRecord.author.set()


async def res_step(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    user_data = await state.get_data()
    await jokes.recordJoke(user_data["joke"], user_data["author"], message.from_user.id)
    await state.update_data(quantity = await jokes.quantityJokesUser(message.from_user.id))
    user_data = await state.get_data()
    await message.answer(
        f"Записано {user_data['quantity']}/10", reply_markup=kb_client
    )
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_start, Text(equals="В главное меню"))
    dp.register_message_handler(
        random_bot_joke, Text(equals="Шутку пользователей бота")
    )
    dp.register_message_handler(random_joke, Text(equals="Шутку рандомную из инета"))
    dp.register_message_handler(my_joke, Text(equals="Мои шутки"))
    dp.register_message_handler(delet_step, Text(equals="Удалить мои Шутки"), state="*")
    dp.register_message_handler(
        delete_res, Text(equals="Подтверждаю"), state=ClientDelete.aon
    )
    dp.register_message_handler(joke_step, Text(equals="Записать шутку"), state="*")
    dp.register_message_handler(
        author_step, state=ClientRecord.joke, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(
        res_step, state=ClientRecord.author, content_types=types.ContentTypes.TEXT
    )
