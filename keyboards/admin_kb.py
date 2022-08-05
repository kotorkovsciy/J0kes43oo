from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb0 = KeyboardButton('Очистка бд')
Kb1 = KeyboardButton('Добавить админа')
kb2 = KeyboardButton('Удалить админа')
kb3 = KeyboardButton('Список админов')
kb4 = KeyboardButton('В главное меню')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(kb0).insert(Kb1).add(kb2).insert(kb3).add(kb4)
