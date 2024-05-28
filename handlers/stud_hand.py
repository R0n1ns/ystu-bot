import asyncio
from contextlib import suppress

from aiogram import types,Router,F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from buttons.abb_buts import quest_buts
from db.db import if_fav_stud, add_fav_stud, if_notif, swith_evd, swith_evw, swith_evl, get_qeust_from_user, add_qeust
from tools.lists import groups

#импорт кнопок
from buttons.stud_buts import *
from tools.scheld_stud import scheld_today, scheld_tomorrow, scheld_next_week, scheld_week

#создание диспатчера
us_rout = Router()



#глвное меню студента
@us_rout.callback_query(F.data =="stud_mod")
@us_rout.message(Command('stud'))
async def main_stud(query: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(query, types.Message):
        # Это команда
        message = query
    else:
        # Это callback-запрос
        message = query.message
    await message.answer(text='Привет студент\nРадуйся жизни пока не отчислили.',
                                  reply_markup=main_stud_buts.as_markup())
    await state.clear()
    # await callback.message.delete() #теперь сообщение с выбором режима удаляется


##################################### fsm для отправки распписания ##########################################
class get_scheld(StatesGroup):
    group = State()
    date = State()
    fav = State()
    ntf = State()

#выбор группы для получения расписания
@us_rout.callback_query(StateFilter(None),F.data == "scheld")
async def scheld_group(callback: types.CallbackQuery, state: FSMContext):
    r = await if_fav_stud(callback.from_user.id)
    if r == False or r == "No":
        await callback.message.answer(text='Если ты хочешь получить расписание,то напиши название своей группы снизу.'
                                           '\nЭто должно выглядеть примерно так: '
                                           '\nцис-16 или сар-44',reply_markup=scheld_buts.as_markup(resize_keyboard=True))
        await state.set_state(get_scheld.group)
    else:
        await callback.message.answer(text=f'Ваша группа {r}.',
                                      reply_markup=scheld_buts.as_markup(resize_keyboard=True))
        await state.set_state(get_scheld.group)
        await scheld_date(callback.message,state,group = r)

@us_rout.message(get_scheld.group,F.text)
async def scheld_date(message: Message, state: FSMContext,group=False):
    if group:
        await message.answer(text='Пожалуйста выберите дату',
                             reply_markup=scheld_date_buts.as_markup(resize_keyboard=True))
        await state.set_state(get_scheld.date)
        await state.update_data(group=group)
    elif message.text.lower() in await groups():
        await message.answer(text='Пожалуйста выберите дату',
                             reply_markup=scheld_date_buts.as_markup(resize_keyboard=True))
        await state.set_state(get_scheld.date)
        await state.update_data(group = message.text.lower())
    else:
        await message.answer(text='Такой группы нет')
        await state.set_state(get_scheld.group)



@us_rout.message(get_scheld.date)
async def scheld(message: Message, state: FSMContext):
    data =await state.get_data()
    group = data['group']
    date = message.text.lower()
    await message.answer(text='Дата и группа приняты.', reply_markup=types.ReplyKeyboardRemove())
    if date == 'сегодня':
        sch = await scheld_today(group)
        if not((sch ==0) or (sch == None)):
            lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in sch['lessons']])
            sch_ = f"{sch['info']['name']}\nПары на день:\n"+lessons
        else:
            sch_ = "на расслабоне🎆"
        # print(sch_)
    elif date == 'завтра':
        sch = await scheld_tomorrow(group)
        if not((sch ==0) or (sch == None)):
            lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in sch['lessons']])
            sch_ = f"{sch['info']['name']}\nПары на день:\n"+lessons
        else:
            sch_ = "на расслабоне🎆"
        # print(sch_)
    elif date == 'эта неделя':
        sch = await scheld_week(group)
        if not((sch ==0) or (sch == None)):
            res = []
            for j in sch:
                lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in j['lessons']])
                k = f"{j['info']['name']}\nПары на день:\n"+lessons
                res.append(k)
            sch_ = "".join(res)
        else:
            sch_ = "на расслабоне🎆"
        # print(sch_)
    elif date == 'cлед неделя':
        sch = await scheld_next_week(group)
        if not((sch ==0) or (sch == None)):
            res = []
            for j in sch:
                lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in j['lessons']])
                k = f"{j['info']['name']}\nПары на день:\n" + lessons
                res.append(k)
            sch_ = "".join(res)
        else:
            sch_ = "на расслабоне🎆"
        # print(sch_)
        # print(sch_)
    r=await if_fav_stud(message.from_user.id)
    if r == False :
        await message.answer(
            text=sch_
        )
        await message.answer(
            text="Добавить группу в избранное?\n"
                 "Группу не нужно будет вводить при запросе расписания\n"
                 "Также можно будет подключить уведомления",
            reply_markup=fav_.as_markup(resize_keyboard=True)
        )
        await state.set_state(get_scheld.fav)
    else:
        await message.answer(
            text=sch_, reply_markup=scheld_buts.as_markup(resize_keyboard=True)
        )
        await state.clear()



@us_rout.message(get_scheld.fav)
async def fav(message: Message, state: FSMContext):
    answ = message.text
    data = await state.get_data()
    group = data['group']
    await message.answer(text='Понял', reply_markup=types.ReplyKeyboardRemove())
    if answ == 'Да)':
        await message.answer(text="Будет сделано!", reply_markup=scheld_buts.as_markup(resize_keyboard=True))

        await add_fav_stud(message.from_user.id,group)

        us = await if_notif(message.from_user.id,group)  # [False,True,False]
        # Фаворитные группы
        ntf_ = InlineKeyboardBuilder()
        ntf_.row(InlineKeyboardButton(text=('❌' if us[0] == False else '✅') + 'Каждую неделю', callback_data="evw"))
        ntf_.row(InlineKeyboardButton(text=('❌' if us[1] == False else '✅') + 'Каждый день', callback_data="evd"))
        ntf_.add(InlineKeyboardButton(text=('❌' if us[2] == False else '✅') + 'Каждую пару', callback_data="evl"))
        ntf_.row(InlineKeyboardButton(text='В меню', callback_data="stud_mod"))

        await message.answer(text='Хотите подключить уведомления?\n'
                                  'Выберите пункт:', reply_markup=ntf_.as_markup(resize_keyboard=True))
        await state.clear()
        # await state.set_state(get_scheld.ntf)
    elif answ == "Нет(":
        await message.answer(text="Хорошо(\n"
                                  "Вы всегда можете добавить группу в настройках.\n"
                                  "Также в настройка можно подключить уведомления",
                             reply_markup=scheld_buts.as_markup(resize_keyboard=True))

        await add_fav_stud(message.from_user.id, "No")
        # await state.set_state(get_scheld.ntf)


@us_rout.callback_query(lambda query: query.data in ['evw', 'evd', 'evl'])
async def ev_n(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    us = await if_notif(user_id)
    # Обработка нажатия на кнопку
    if callback.data == "evw":
            if us[0] == False:
                await swith_evw(callback.from_user.id,'on')
                us[0] = True
            else:
                await swith_evw(callback.from_user.id, 'off')
                us[0] = False
    elif callback.data == "evd":
            if us[1] == False:
                await swith_evd(callback.from_user.id, 'on')
                us[1] = True
            else:
                await swith_evd(callback.from_user.id, 'off')
                us[1] = False
    elif callback.data == "evl":
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
        [InlineKeyboardButton(text='В меню', callback_data="stud_mod")]
    ], )

    await callback.message.edit_text(text='Хотите подключить уведомления?\n'
                                 'Выберите пункт: ', reply_markup=ntf_)



##################################### fsm для отправки распписания ##########################################
#вопрос
@us_rout.callback_query(F.data == "ask_quest_")
async def quest_(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет !\n'
                                       'Хочешь задать вопрос или посмотреть свои вопросы?',
                                  reply_markup=quest_buts_.as_markup(resize_keyboard=True))
    await callback.message.delete()
################заданные вопросы################
@us_rout.callback_query(F.data == "questions_")
async def questions_(callback: types.CallbackQuery):
    all_ = await get_qeust_from_user(callback.from_user.id)
    slvd = await get_qeust_from_user(callback.from_user.id,'slvd')
    unslvd = await get_qeust_from_user(callback.from_user.id, 'unslvd')
    if all_:
        await callback.message.answer(text=f'У вас {len(all_)} вопросов\n'
                                           f'Решенных : {len(slvd)}\n'
                                           f'Не решенных : {len(unslvd)}\n\n'
                                           'Какие вопросы хотите вывести?',
                                      reply_markup=questions__.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='У вас нет вопросов(',
                                      reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await callback.message.delete()

@us_rout.callback_query(F.data == "solved_quest_")
async def solved_quest_(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id,'slvd')
    if quests!=[]:
        for quest in quests:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}\n"
                                               f"Ответ: \n {quest['answer']}\n")
        await callback.message.answer(text='Готово!',
                                      reply_markup=not_quests_.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='Решенных вопросов нет!',
                                      reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await callback.message.delete()
@us_rout.callback_query(F.data == "unsolved_quest_")
async def unsolved_quest_(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id, 'unslvd')
    if quests:
        for quest in quests:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}")
        await callback.message.answer(text='Готово!',
                                      reply_markup=not_quests_.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='Не решенных вопросов нет!',
                                      reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await callback.message.delete()

@us_rout.callback_query(F.data == "all_quest_")
async def all_quest_(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id)
    for quest in quests:
        if quest['resolved']:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}\n"
                                               f"Ответ: \n {quest['answer']}\n")
        else:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}")
    await callback.message.answer(text='Готово!',
                                  reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await callback.message.delete()

################заданные вопросы################

################задать вопрос################

class add_quest__(StatesGroup):
    text = State()
@us_rout.callback_query(StateFilter(None),F.data == "add_quest_")
async def add_quest_(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста напишие текст вашего запроса!\n'
                                       'Текст не должен быть больше 300 символов,\n'
                                       'А также не нужен содержать нецензурную лексику.',
                                  reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await state.set_state(add_quest__.text)

@us_rout.message(add_quest__.text,F.text)
async def add_text_q_(message: Message, state: FSMContext):
    text = message.text.lower()
    if len(text)>300:
        await message.answer(text='Текст будет обрезаан до 300 символов.')
        text = text[:300]
    await message.answer(text='Текст принят ,ожидайте ответа!',
                         reply_markup=not_quests_.as_markup(resize_keyboard=True))
    await add_qeust(message.from_user.id,text)

    await state.clear()
################задать вопрос################



@us_rout.callback_query(F.data == "departments")
async def departments(callback: types.CallbackQuery):
        await callback.message.answer(text='Кафедры:',
                                      reply_markup=departments_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()

@us_rout.callback_query(F.data == "news")
async def news(callback: types.CallbackQuery):
        await callback.message.answer(text='Новости:',
                                      reply_markup=news_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()

@us_rout.callback_query(F.data == "institutes")
async def institutes(callback: types.CallbackQuery):
        await callback.message.answer(text='Институты:',
                                      reply_markup=institutes_buts.as_markup(resize_keyboard=True))
        await callback.message.delete()

@us_rout.callback_query(F.data == "soc_net")
async def soc_net(callback: types.CallbackQuery):
    await callback.message.answer(text='Социальные сети:',
                                  reply_markup=socnet_buts.as_markup(resize_keyboard=True))
    await callback.message.delete()

