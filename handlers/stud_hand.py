import asyncio
from aiogram import types,Router,F
from aiogram.filters.command import Command
#импорт кнопок
from buttons.stud_buts import *
#создание диспатчера
us_rout = Router()


@us_rout.callback_query(F.data == "stud_mod")
async def main_stud(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет студент\nРадуйся жизни пока не отчислили.',
                                  reply_markup=main_stud_buts.as_markup())
    await callback.message.delete()

