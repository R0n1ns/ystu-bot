from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопка основного меню студента
main_stud_=[["Расписание","scheld"],["Оставить отзыв","revie"],["Соц сети","soc_net"],["Нофости","news"]]
#инциаизация клавиатуры
main_stud_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in main_stud_:
    main_stud_buts.row(InlineKeyboardButton(text=i[0], callback_data=i[1]))