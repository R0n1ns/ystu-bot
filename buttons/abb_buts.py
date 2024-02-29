from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопка основного меню аббитуриента
main_abb_=[["Направления обучения","majors"],["Задать вопрос","ask_quest"],["Соц сети","soc_net"],["Нофости","news"],["Соц сети","soc_net"],["Приемная коммиссия","committee"]]
#инциаизация клавиатуры
main_abb_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in main_abb_:
    main_abb_buts.row(InlineKeyboardButton(text=i[0], callback_data=i[1]))