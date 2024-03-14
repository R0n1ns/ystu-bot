from aiogram import types,Router
from aiogram.filters.command import Command,CommandStart
#импорт кнопок
from buttons.other_buts import *
#создание диспатчера
oth_rout=Router()

@oth_rout.message(Command('check'))
async def check(message: types.Message):
    await message.answer(text='Привет!\nПожалуйста выбери режим в который вы хотете получить доступ.',
                         reply_markup = check_buts.as_markup())

#диспатчер start
@oth_rout.message(Command('start'))
async def start_hand(message: types.Message):
    await message.answer(text='Привет!\nПожалуйста выбери режим работы бота.',
                         reply_markup = start_buts.as_markup())
    await message.delete()


#
# @oth_rout.message(Command('change_mode'))
# async def change_mode_hand(message: types.Message):