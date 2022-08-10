from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BadRequest
from create_bot import adm_sql
from os import getenv, remove
from keyboards import kb_admin, kb_aon, kb_record


class AdminDelete(StatesGroup):
    user_id = State()
    aon = State()


class AddAdmin(StatesGroup):
    inviting = State()
    name = State()
    user_id = State()


class DelAdmin(StatesGroup):
    responsible = State()
    user_id = State()


async def cmd_start_adm(message: types.Message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await message.answer("Вы в админской", reply_markup=kb_admin)


async def step_clear_database(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await AdminDelete.user_id.set()
            await state.update_data(user_id=user_id)
            await message.answer("Вы уверены ?", reply_markup=kb_aon)
            await AdminDelete.aon.set()


async def res_clear_database(message: types.Message, state: FSMContext):
    await adm_sql.deleteJokes()
    await state.finish()
    await message.answer("🗑 Была произведена очистка 🗑", reply_markup=kb_admin)


async def step_add_admin(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await AddAdmin.inviting.set()
            await state.update_data(inviting=user_id)
            await message.answer("Введите имя добавляемого админа", reply_markup=kb_record)
            await AddAdmin.name.set()


async def step_name_admin(message: types.Message, state: FSMContext):
    if await adm_sql.nameAdminExists(message.text):
        await message.answer("Такое имя уже занято! Введите другое", reply_markup=kb_record)
        return
    await state.update_data(name=message.text)
    await message.answer("Введите id добавляемого админа", reply_markup=kb_record)
    await AddAdmin.user_id.set()


async def res_add_admin(message: types.Message, state: FSMContext):
    user_id = ''.join([i for i in message.text if i.isdigit()])
    if not user_id:
        await message.answer("Некорректный id! Введите снова", reply_markup=kb_record)
        return
    await state.update_data(user_id=int(user_id))
    user_data = await state.get_data()
    if await adm_sql.adminExists(user_data["user_id"]):
        await message.answer("Админ с таким id уже существует!")
        await state.finish()
    await adm_sql.adminAdd(user_data["user_id"], user_data["name"], user_data["inviting"])
    await message.answer("Админ добавлен", reply_markup=kb_admin)
    await state.finish()


async def step_del_admin(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await DelAdmin.responsible.set()
            await state.update_data(responsible=user_id)
            await message.answer("Введите id удаляемого админа", reply_markup=kb_record)
            await DelAdmin.user_id.set()


async def res_del_admin(message: types.Message, state: FSMContext):
    user_id = ''.join([i for i in message.text if i.isdigit()])
    if not user_id:
        await message.answer("Некорректный id! Введите снова", reply_markup=kb_record)
        return
    await state.update_data(user_id=int(user_id))
    user_data = await state.get_data()
    if not await adm_sql.adminExists(user_data["user_id"]):
        await message.answer("Админ с таким id не существует!", reply_markup=kb_record)
        return
    await adm_sql.adminDel(user_data["user_id"])
    await message.answer("Админ удалён", reply_markup=kb_admin)
    await state.finish()


async def sql_damp(message: types.Message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await adm_sql.dump(user_id)
            try:
                file = open(f"sql\dump_users_{user_id}.sql", 'rb')
                await message.answer_document(file, caption="sql dump users")
            except BadRequest:
                await message.answer("Пока что дамп бд users не возможен", reply_markup=kb_admin)
            try:
                file = open(f"sql\dump_jokes_{user_id}.sql", 'rb')
                await message.answer_document(file, caption="sql dump jokes")
            except BadRequest:
                await message.answer("Пока что дамп бд jokes не возможен", reply_markup=kb_admin)
            try:
                file = open(f"sql\dump_admins_{user_id}.sql", 'rb')
                await message.answer_document(file, caption="sql dump admins")
            except BadRequest:
                await message.answer("Пока что дамп бд admins не возможен", reply_markup=kb_admin)
            remove(f"sql\dump_users_{user_id}.sql")
            remove(f"sql\dump_jokes_{user_id}.sql")
            remove(f"sql\dump_admins_{user_id}.sql")


async def all_admins(message: types.Message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if int(getenv("ID_ADMIN")) == user_id or await adm_sql.adminExists(user_id):
            await message.answer(await adm_sql.allAdmins())


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_start_adm, commands="start_adm")
    dp.register_message_handler(step_clear_database, Text(
        equals="Очистка бд"), state="*")
    dp.register_message_handler(res_clear_database, Text(
        equals='Подтверждаю'), state=AdminDelete.aon)
    dp.register_message_handler(step_add_admin, Text(
        equals="Добавить админа"), state="*")
    dp.register_message_handler(
        step_name_admin, state=AddAdmin.name, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(
        res_add_admin, state=AddAdmin.user_id, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(step_del_admin, Text(
        equals="Удалить админа"), state="*")
    dp.register_message_handler(
        res_del_admin, state=DelAdmin.user_id, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(sql_damp, Text(
        equals="Дамп бд"))
    dp.register_message_handler(all_admins, Text(
        equals="Список админов"))
