from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопки start
start=[["Студент","stud_mod"],["Аббитуриент","abb_mod"]]
#инциаизация клавиатуры
start_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in start:
    start_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))
