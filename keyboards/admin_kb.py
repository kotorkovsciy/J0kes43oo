from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb0 = KeyboardButton('Очистка бд')
kb1 = KeyboardButton('Дамп бд')
kb2 = KeyboardButton('В главное меню')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(kb0).add(kb1).add(kb2)
