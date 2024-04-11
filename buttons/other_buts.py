from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup ,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder ,ReplyKeyboardBuilder

#кнопки start
start=[["Студент","stud_mod"],["Аббитуриент","abb_mod"]]
#инциаизация клавиатуры
start_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in start:
    start_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))

#кнопки check
check=[["Преподователь","teach_check"],["Администратор","adm_check"]]
#инциаизация клавиатуры
check_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in check:
    check_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))

#кнопки settings
settings_=[["Фаворитная группа","fav_group"]]
#инциаизация клавиатуры
settings_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in settings_:
    settings_buts.add(InlineKeyboardButton(text=i[0], callback_data=i[1]))


sett_ = InlineKeyboardBuilder()
sett_.add(InlineKeyboardButton(text="В настройки", callback_data= 'settings'))

del_fav = ReplyKeyboardBuilder()
del_fav.add(KeyboardButton(text="Удалить"))