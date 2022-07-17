from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb0 = KeyboardButton('Записать шутку')
kb1 = KeyboardButton('Шутку пользователей бота')
kb2 = KeyboardButton('Шутку рандомную из инета')
kb3 = KeyboardButton('Мои шутки')
kb4 = KeyboardButton('Удалить мои Шутки')
kb5 = KeyboardButton('Отмена')
kb6 = KeyboardButton('Да')
kb7 = KeyboardButton('Нет')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(kb0).add(kb1).insert(kb2).add(kb3).insert(kb4)

kb_record = ReplyKeyboardMarkup(resize_keyboard=True)

kb_record.add(kb5)

kb_aon = ReplyKeyboardMarkup(resize_keyboard=True)

kb_aon.add(kb6).add(kb7)
