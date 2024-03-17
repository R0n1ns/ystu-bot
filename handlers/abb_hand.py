import asyncio
from aiogram import types,Router,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
#импорт кнопок
from buttons.abb_buts import *
from buttons.stud_buts import socnet_buts, departments_buts

#создание диспатчера
add_rout = Router()

@add_rout.callback_query(F.data == "abb_mod")
async def main_stud(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет аббитуриент\nРадоваться рано,ты еще не поступил.',
                                  reply_markup=main_abb_buts.as_markup())
    await callback.message.delete()


#вывод соцсетей
@add_rout.callback_query(F.data == "soc_net_abb")
async def soc_net_abb(callback: types.CallbackQuery):
    await callback.message.answer(text='Социальные сети:',
                                  reply_markup=socnet_abb_buts.as_markup(resize_keyboard=True))
    await callback.message.delete()


@add_rout.callback_query(F.data == "departments_abb")
async def departments_abb(callback: types.CallbackQuery):
        await callback.message.answer(text='Кафедры:',
                                      reply_markup=departments_abb_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()

@add_rout.callback_query(F.data == "news_abb")
async def news_abb(callback: types.CallbackQuery):
        await callback.message.answer(text='Новости:',
                                      reply_markup=news_abb_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()

@add_rout.callback_query(F.data == "institutes_abb")
async def institutes_abb(callback: types.CallbackQuery):
        await callback.message.answer(text='Институты:',
                                      reply_markup=institutes_abb_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()