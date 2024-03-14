import asyncio
from aiogram import types,Router,F
import phonenumbers
from aiogram.filters.command import Command
#импорт кнопок
from buttons.teach_buts import *
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from db.db import teach_if, teach_add_tg_id
from handlers.other_hand import check

#создание диспатчера
teach_rout = Router()

class TeachHandler(StatesGroup):
    teach = State()

@teach_rout.callback_query(F.data == "teach_check")
async def teach_check(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Для того чтобы получить доступ,пожалуйста войдете по вашему номеру.\n'
                                       'Это можно нажав кнопку снизу.',
                                  reply_markup=check_teach_buts.as_markup(resize_keyboard=True))
    await state.set_state(TeachHandler.teach)

@teach_rout.message(TeachHandler.teach)
async def teach_(message: Message, state: FSMContext):
    us_id = message.contact.user_id
    phone = phonenumbers.parse(message.contact.phone_number).national_number
    f =await teach_if(phone)
    if us_id == message.from_user.id and f:
        await teach_add_tg_id(phone,us_id)
        await message.answer(text='Проверка успешно пройдена',reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        await message.answer(text='Теперь ввы можете перейти в меню.',reply_markup=menu_.as_markup(resize_keyboard=True))
    elif us_id == message.from_user.id and f==False:
        await message.answer('Записи с таким номером нет(',reply_markup=types.ReplyKeyboardRemove())
        await check(message)
        await state.clear()
    else :
        await message.answer(text='Пожалуйста отправьте свой контакт по кнопке ниже.')
        await state.set_state(TeachHandler.teach)


@teach_rout.callback_query(F.data == "main_teach")
async def teach_main(callback: types.CallbackQuery):
    await callback.message.answer(text='Здравствуйте,это главное меню.',
                                  reply_markup=menu_buts.as_markup(resize_keyboard=True))