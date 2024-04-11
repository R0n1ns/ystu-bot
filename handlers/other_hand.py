from aiogram import types,Router,F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command,CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

#импорт кнопок
from buttons.other_buts import *
from db.db import replace_fav_stud
from tools.lists import groups

#создание диспатчера
oth_rout=Router()

@oth_rout.message((Command('settings')) or (F.data =='settings'))
async def settings(message: types.Message):
    await message.answer(text='Привет!\nПожалуйста выберите что хотите изменить:',
                         reply_markup = settings_buts.as_markup(resize_keyboard=True))
    await message.delete()

@oth_rout.message(Command('check'))
async def check(message: types.Message):
    await message.answer(text='Привет!\nПожалуйста выбери режим в который вы хотете получить доступ.',
                         reply_markup = check_buts.as_markup(resize_keyboard=True))



#диспатчер start
@oth_rout.message(Command('start'))
async def start_hand(message: types.Message):
    await message.answer(text='Привет!\nПожалуйста выбери режим работы бота.',
                         reply_markup = start_buts.as_markup(resize_keyboard=True))
    await message.delete()




class fav_res(StatesGroup):
    group = State()
@oth_rout.callback_query(StateFilter(None),F.data == "fav_group")
async def fav__(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(text='Если вы хотите сменить группу,то введите ее название.\n'
                                           'Если вы хотите удалить группу,то нажмите кнопку снизу.',
                         reply_markup = del_fav.as_markup(resize_keyboard=True))
        await state.set_state(fav_res.group)

@oth_rout.message(fav_res.group,F.text)
async def fav_change(message: Message, state: FSMContext):
    id = message.from_user.id
    if message.text.lower() == "удалить":
        await replace_fav_stud(id, "No")
        await state.clear()
        await message.answer(text='Принял', reply_markup=types.ReplyKeyboardRemove())
        # await message.answer(text='Все готово!')
        await settings(message)
    elif message.text.lower() in await groups():
        await replace_fav_stud(id, str(message.text.lower()))
        await message.answer(text='Принял', reply_markup=types.ReplyKeyboardRemove())
        # await message.answer(text='Все готово!')
        await state.clear()
        await settings(message)
    else:
        await message.answer(text='Такой группы нет')
        await state.set_state(fav_res.group)

#
# @oth_rout.message(Command('change_mode'))
# async def change_mode_hand(message: types.Message):