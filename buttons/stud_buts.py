from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup ,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder ,ReplyKeyboardBuilder

#кнопка основного меню студента
main_stud_=[["Расписание","scheld"],["Отзывы","revie"],["Соц сети","soc_net"],["О вузе","news"]]
#инциаизация клавиатуры
main_stud_buts = InlineKeyboardBuilder()
#генерация клавиатуры
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[0][0],callback_data=main_stud_[0][1]))
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[1][0],callback_data=main_stud_[1][1]))
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[2][0],callback_data=main_stud_[2][1]))
main_stud_buts.add(InlineKeyboardButton(text=main_stud_[3][0],callback_data=main_stud_[3][1]))

#кнопка основного выбора даты для рассписания
scheld_date=["Сегодня","Завтра","Эта неделя","Cлед неделя"]
#инциаизация клавиатуры
scheld_date_buts = ReplyKeyboardBuilder()
#генерация клавиатуры
scheld_date_buts.row(KeyboardButton(text=scheld_date[0]))
scheld_date_buts.add(KeyboardButton(text=scheld_date[1]))
scheld_date_buts.row(KeyboardButton(text=scheld_date[2]))
scheld_date_buts.add(KeyboardButton(text=scheld_date[3]))


#кнопка основного выбора даты для рассписания
scheld_=[["В главное меню.",'stud_mod']]
#инциаизация клавиатуры
scheld_buts = InlineKeyboardBuilder()
#генерация клавиатуры
scheld_buts.row(InlineKeyboardButton(text=scheld_[0][0],callback_data=scheld_[0][1]))
