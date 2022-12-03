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


class IsAdmin:
    def __init__(self, user_id):
        self.__set_id__(user_id)

    @classmethod
    def __set_id__(cls, user_id):
        cls.user_id = user_id

    @classmethod
    def __get_id__(cls):
        return cls.user_id

    user_id = property(__get_id__, __set_id__)

    @classmethod
    async def is_admin(cls):
        if int(getenv("ID_ADMIN")) == cls.user_id or await adm_sql.adminExists(cls.user_id):
            return True
        else:
            return False

    @classmethod
    async def prv_is_admin(cls, chat_type):
        if chat_type == "private":
            if int(getenv("ID_ADMIN")) == cls.user_id or await adm_sql.adminExists(cls.user_id):
                return True
            else:
                return False
        else:
            return False


async def cmd_start_adm(message: types.Message):
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        await message.answer("Вы в админской", reply_markup=kb_admin)


async def step_clear_database(message: types.Message, state: FSMContext):
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        await AdminDelete.user_id.set()
        await state.update_data(user_id=message.from_user.id)
        await message.answer("Вы уверены ?", reply_markup=kb_aon)
        await AdminDelete.aon.set()


async def res_clear_database(message: types.Message, state: FSMContext):
    await adm_sql.deleteJokes()
    await state.finish()
    await message.answer("🗑 Была произведена очистка 🗑", reply_markup=kb_admin)


async def step_add_admin(message: types.Message, state: FSMContext):
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        await AddAdmin.inviting.set()
        await state.update_data(inviting=message.from_user.id)
        await message.answer(
          "Введите имя добавляемого админа", reply_markup=kb_record
        )
        await AddAdmin.name.set()


async def step_name_admin(message: types.Message, state: FSMContext):
    if await adm_sql.nameAdminExists(message.text):
        await message.answer(
            "Такое имя уже занято! Введите другое", reply_markup=kb_record
        )
        return
    await state.update_data(name=message.text)
    await message.answer("Введите id добавляемого админа", reply_markup=kb_record)
    await AddAdmin.user_id.set()


async def res_add_admin(message: types.Message, state: FSMContext):
    user_id = "".join([i for i in message.text if i.isdigit()])
    if not user_id:
        await message.answer("Некорректный id! Введите снова", reply_markup=kb_record)
        return
    await state.update_data(user_id=int(user_id))
    user_data = await state.get_data()
    if await adm_sql.adminExists(user_data["user_id"]):
        await message.answer("Админ с таким id уже существует!")
        await state.finish()
    await adm_sql.adminAdd(
        user_data["user_id"], user_data["name"], user_data["inviting"]
    )
    await message.answer("Админ добавлен", reply_markup=kb_admin)
    await state.finish()


async def step_del_admin(message: types.Message, state: FSMContext):
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        await DelAdmin.responsible.set()
        await state.update_data(responsible=message.from_user.id)
        await message.answer("Введите id удаляемого админа", reply_markup=kb_record)
        await DelAdmin.user_id.set()


async def res_del_admin(message: types.Message, state: FSMContext):
    user_id = "".join([i for i in message.text if i.isdigit()])
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
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        user_id = message.from_user.id
        await adm_sql.dump(user_id)
        try:
            file = open(f"sql\dump_users_{user_id}.sql", "rb")
            await message.answer_document(file, caption="sql dump users")
        except BadRequest:
            await message.answer(
                "Пока что дамп бд users не возможен", reply_markup=kb_admin
            )
        try:
            file = open(f"sql\dump_jokes_{user_id}.sql", "rb")
            await message.answer_document(file, caption="sql dump jokes")
        except BadRequest:
            await message.answer(
                "Пока что дамп бд jokes не возможен", reply_markup=kb_admin
            )
        try:
            file = open(f"sql\dump_admins_{user_id}.sql", "rb")
            await message.answer_document(file, caption="sql dump admins")
        except BadRequest:
            await message.answer(
                "Пока что дамп бд admins не возможен", reply_markup=kb_admin
            )
        remove(f"sql\dump_users_{user_id}.sql")
        remove(f"sql\dump_jokes_{user_id}.sql")
        remove(f"sql\dump_admins_{user_id}.sql")


async def all_admins(message: types.Message):
    if await IsAdmin(message.from_user.id).prv_is_admin(message.chat.type):
        await message.answer(await adm_sql.allAdmins())


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_start_adm, commands="start_adm")
    dp.register_message_handler(
        step_clear_database, Text(equals="Очистка бд"), state="*"
    )
    dp.register_message_handler(
        res_clear_database, Text(equals="Подтверждаю"), state=AdminDelete.aon
    )
    dp.register_message_handler(
        step_add_admin, Text(equals="Добавить админа"), state="*"
    )
    dp.register_message_handler(
        step_name_admin, state=AddAdmin.name, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(
        res_add_admin, state=AddAdmin.user_id, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(
        step_del_admin, Text(equals="Удалить админа"), state="*"
    )
    dp.register_message_handler(
        res_del_admin, state=DelAdmin.user_id, content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(sql_damp, Text(equals="Дамп бд"))
    dp.register_message_handler(all_admins, Text(equals="Список админов"))
