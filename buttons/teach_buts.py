from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

#инциаизация клавиатуры
check_teach_buts = ReplyKeyboardBuilder()
#генерация клавиатуры
check_teach_buts.add(KeyboardButton(text="Подтвердить номер", request_contact=True))

#инциаизация клавиатуры
menu_buts = InlineKeyboardBuilder()
#генерация клавиатуры
menu_buts.add(InlineKeyboardButton(text="Расписание", callback_data="abb_mod"))

#инциаизация клавиатуры
menu_ = InlineKeyboardBuilder()
#генерация клавиатуры
menu_.add(InlineKeyboardButton(text="Перейти в меню.", callback_data="main_teach"))

