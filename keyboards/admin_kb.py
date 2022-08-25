from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb0 = KeyboardButton("Очистка бд")
kb1 = KeyboardButton("Дамп бд")
kb2 = KeyboardButton("Добавить админа")
kb3 = KeyboardButton("Удалить админа")
kb4 = KeyboardButton("Список админов")
kb5 = KeyboardButton("В главное меню")


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(kb0).insert(kb1).add(kb2).insert(kb3).add(kb4).add(kb5)
