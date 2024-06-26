from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup ,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder ,ReplyKeyboardBuilder

#кнопки start
start=[["Студент","stud_mod"],["Аббитуриент","abb_mod"]]
#инциаизация клавиатуры
start_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in start:
    start_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))

#кнопки settings
settings_=[["Фаворитная группа","fav_group"],["Уведомления","notf_"]]
#инциаизация клавиатуры
settings_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in settings_:
    settings_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))


sett_ = InlineKeyboardBuilder()
sett_.add(InlineKeyboardButton(text="В настройки", callback_data= 'settings'))

del_fav = ReplyKeyboardBuilder()
del_fav.add(KeyboardButton(text="Удалить"))

about_ = InlineKeyboardBuilder()
about_.row(InlineKeyboardButton(text="гитхаб",url='https://github.com/R0n1ns/ystu-bot'))
about_.row(InlineKeyboardButton(text="Команда",callback_data='team'))

back_ab = InlineKeyboardBuilder()
back_ab.row(InlineKeyboardButton(text="Назад",callback_data='about'))

back_to_main = InlineKeyboardBuilder()
back_to_main.row(InlineKeyboardButton(text="Вернуться в главное менюю",callback_data='back_to_main'))

notf_ = InlineKeyboardBuilder()
notf_.row(InlineKeyboardButton(text="Задать фаворитную группу",callback_data='fav_group'))
notf_.row(InlineKeyboardButton(text="В меню",callback_data='settings'))
