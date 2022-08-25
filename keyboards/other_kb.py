from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb5 = KeyboardButton("Отмена")
kb6 = KeyboardButton("Подтверждаю")


kb_record = ReplyKeyboardMarkup(resize_keyboard=True)

kb_record.add(kb5)

kb_aon = ReplyKeyboardMarkup(resize_keyboard=True)

kb_aon.add(kb6).add(kb5)
