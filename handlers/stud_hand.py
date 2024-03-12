import asyncio
from aiogram import types,Router,F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from tools.lists import groups

#импорт кнопок
from buttons.stud_buts import *
from tools.scheld_stud import scheld_today, scheld_tomorrow, scheld_next_week, scheld_week

#создание диспатчера
us_rout = Router()

#глвное меню студента
@us_rout.callback_query(F.data == "stud_mod")
async def main_stud(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет студент\nРадуйся жизни пока не отчислили.',
                                  reply_markup=main_stud_buts.as_markup())


#fsm для отправки распписания
class get_scheld(StatesGroup):
    group = State()
    date = State()

#выбор группы для получения расписания
@us_rout.callback_query(StateFilter(None),F.data == "scheld")
async def scheld_group(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Если ты хочешь получить расписание,то напиши название своей группы снизу.'
                                       '\nЭто должно выглядеть примерно так: '
                                       '\nцис-16 или сар-44')
    await state.set_state(get_scheld.group)

@us_rout.message(get_scheld.group,F.text)
async def scheld_date(message: Message, state: FSMContext):
    if message.text.lower() in await groups():
        await message.answer(text='Пожалуйста выберите дату',
                             reply_markup=scheld_date_buts.as_markup(resize_keyboard=True))
        await state.set_state(get_scheld.date)
        await state.update_data(group = message.text.lower())
    else:
        await message.answer(text='Такой группы нет')
        await state.set_state(get_scheld.group)

# @us_rout.message(get_scheld.date,F.text)
# async def take_date(message: Message, state: FSMContext):
#     await message.answer(text='Дата и группа приняты.',reply_markup=types.ReplyKeyboardRemove())
#     await state.update_data(date = message.text.lower())
#     await state.set_state(get_scheld.scheld)

@us_rout.message(get_scheld.date)
async def scheld(message: Message, state: FSMContext):
    data =await state.get_data()
    group = data['group']
    date = message.text.lower()
    await message.answer(text='Дата и группа приняты.', reply_markup=types.ReplyKeyboardRemove())
    if date == 'сегодня':
        sch = await scheld_today(group)
        lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in sch['lessons']])
        sch_ = f"{sch['info']['name']}\nПары на день:\n"+lessons
        # print(sch_)
    elif date == 'завтра':
        sch = await scheld_tomorrow(group)
        lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in sch['lessons']])
        sch_ = f"{sch['info']['name']}\nПары на день:\n"+lessons
        # print(sch_)
    elif date == 'эта неделя':
        sch = await scheld_week(group)
        res = []
        for j in sch:
            lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in j['lessons']])
            k = f"{j['info']['name']}\nПары на день:\n"+lessons
            res.append(k)
        sch_ = "".join(res)
        # print(sch_)
    elif date == 'cлед неделя':
        sch = await scheld_next_week(group)
        print(1111111111)
        res = []
        for j in sch:
            lessons = "".join([f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n" for i in j['lessons']])
            k = f"{j['info']['name']}\nПары на день:\n" + lessons
            res.append(k)
        sch_ = "".join(res)
        print(sch_)
        # print(sch_)
    await message.answer(
            text=sch_,reply_markup=scheld_buts.as_markup()
        )
    await state.clear()

