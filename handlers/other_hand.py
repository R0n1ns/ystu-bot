from aiogram import types,Router,F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command,CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

#импорт кнопок
from buttons.other_buts import *
from db.db import replace_fav_stud, if_fav_stud, if_notif, swith_evw, swith_evd, swith_evl
from tools.lists import groups

#создание диспатчера
oth_rout=Router()

@oth_rout.callback_query(F.data =="settings")
@oth_rout.message(Command('settings'))
async def settings(query: types.Message | types.CallbackQuery):
    if isinstance(query, types.Message):
        # Это команда
        message = query
    else:
        # Это callback-запрос
        message = query.message

    await message.answer(text='Привет!\nПожалуйста выберите что хотите изменить:',
                         reply_markup = settings_buts.as_markup(resize_keyboard=True))
    await message.delete()

@oth_rout.callback_query(F.data =="about")
@oth_rout.message(Command('about'))
async def about(query: types.Message | types.CallbackQuery):
    if isinstance(query, types.Message):
        # Это команда
        message = query
    else:
        # Это callback-запрос
        message = query.message

    await message.answer(text='Привет!\n'
                              'Этот бот разработан студентами 1го курса\n'
                              'Поэтому хорошо ,если вообще работает',
                         reply_markup = about_.as_markup(resize_keyboard=True))
    await message.delete()

@oth_rout.callback_query(F.data == "team")
async def team(callback: types.CallbackQuery):
    await callback.message.answer(text='Наша команда:\n\n'
                              'Разработчикки:\n'
                              'Коробов Вадим\n'
                              'Вахрамеев Никита\n\n'
                              'Помощники:\n'
                              'Шабалинна Анна\n'
                              'Исаков Данила',
                         reply_markup = back_ab.as_markup(resize_keyboard=True))


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

@oth_rout.callback_query(F.data =="notf")
async def notf(callback: types.CallbackQuery):
    if not(await if_fav_stud(callback.from_user.id)):
            await callback.message.answer(text="Сначало введите группу!",
                                          reply_markup=notf_.as_markup(resize_keyboard=True))
    else:
        us = await if_notif(callback.from_user.id)  # [False,True,False]
        # Фаворитные группы
        ntf_ = InlineKeyboardBuilder()
        ntf_.row(InlineKeyboardButton(text=('❌' if us[0] == False else '✅') + 'Каждую неделю', callback_data="evw_"))
        ntf_.row(InlineKeyboardButton(text=('❌' if us[1] == False else '✅') + 'Каждый день', callback_data="evd_"))
        ntf_.add(InlineKeyboardButton(text=('❌' if us[2] == False else '✅') + 'Каждую пару', callback_data="evl_"))
        ntf_.row(InlineKeyboardButton(text='В меню', callback_data="settings"))

        await callback.message.answer(text='Хотите подключить уведомления?\n'
                                  'Выберите пункт:', reply_markup=ntf_.as_markup(resize_keyboard=True))

@oth_rout.callback_query(lambda query: query.data in ['evw_', 'evd_', 'evl_'])
async def ev_notf(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    us = await if_notif(user_id)
    # Обработка нажатия на кнопку
    if callback.data == "evw_":
            if us[0] == False:
                await swith_evw(callback.from_user.id,'on')
                us[0] = True
            else:
                await swith_evw(callback.from_user.id, 'off')
                us[0] = False
    elif callback.data == "evd_":
            if us[1] == False:
                await swith_evd(callback.from_user.id, 'on')
                us[1] = True
            else:
                await swith_evd(callback.from_user.id, 'off')
                us[1] = False
    elif callback.data == "evl_":
            if us[2] == False:
                await swith_evl(callback.from_user.id, 'on')
                us[2] = True
            else:
                await swith_evl(callback.from_user.id, 'off')
                us[2] = False
    us = await if_notif(user_id)
    # Обновляем сообщение с новой клавиатурой
    # Функция для обновления клавиатуры в сообщении с учетом значений us
    ntf_ = InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=('❌' if not us[0] else '✅') + 'Каждую неделю', callback_data="evw")],[
         types.InlineKeyboardButton(text=('❌' if not us[1] else '✅') + 'Каждый день', callback_data="evd"),
        types.InlineKeyboardButton(text=('❌' if not us[2] else '✅') + 'Каждую пару', callback_data="evl")],
        [InlineKeyboardButton(text='В меню', callback_data="settings")]
    ], )

    await callback.message.edit_text(text='Хотите подключить уведомления?\n'
                                 'Выберите пункт: ', reply_markup=ntf_)

#
# @oth_rout.message(Command('change_mode'))
# async def change_mode_hand(message: types.Message):