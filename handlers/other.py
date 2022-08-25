from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import kb_admin, kb_client


async def cmd_cancel(message: types.Message, state: FSMContext):
    user_get_state = await state.get_state()
    if user_get_state:
        if "Client" in user_get_state:
            await message.answer("Действие отменено", reply_markup=kb_client)
        elif "Admin" in user_get_state:
            await message.answer("Действие отменено", reply_markup=kb_admin)
        await state.finish()
    else:
        await message.answer("Действие отменено", reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
