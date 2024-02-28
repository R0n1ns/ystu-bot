from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопки start
start_buts = InlineKeyboardBuilder()
start_buts.add(InlineKeyboardButton(text="Студент", callback_data="stud_mod"))
start_buts.add(InlineKeyboardButton(text="Аббитуриент", callback_data="abb_mod"))

