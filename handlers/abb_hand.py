import asyncio
from aiogram import types,Router,F
from aiogram.filters.command import Command
#импорт кнопок
from buttons.abb_buts import *
#создание диспатчера
add_rout = Router()

@add_rout.callback_query(F.data == "abb_mod")
async def main_stud(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет аббитуриент\nРадоваться рано,ты еще не поступил.',
                                  reply_markup=main_abb_buts.as_markup())
    await callback.message.delete()