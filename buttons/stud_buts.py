from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопка основного меню студента
main_stud_=[["Расписание","scheld"],["Оставить отзыв","revie"],["Соц сети","soc_net"]]
#инциаизация клавиатуры
main_stud_buts = InlineKeyboardBuilder()
#генерация клавиатуры
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[0][0],callback_data=main_stud_[0][1]))
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[1][0],callback_data=main_stud_[1][1]))
main_stud_buts.add(InlineKeyboardButton(text=main_stud_[2][0],callback_data=main_stud_[2][1]))
