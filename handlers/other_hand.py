from aiogram import types,Router
from aiogram.filters.command import Command,CommandStart
#импорт кнопок
from buttons.other_buts import start_buts
#создание диспатчера
oth_rout=Router()

#диспатчер start
@oth_rout.message(CommandStart)
async def message_handler(message: types.Message):
    await message.answer(text='Приве!\nПожалуйста выбери режим работы бота.',
                         reply_markup = start_buts.as_markup())