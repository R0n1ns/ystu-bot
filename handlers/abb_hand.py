import asyncio
from aiogram import types,Router,F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.types import Message

#импорт кнопок
from buttons.abb_buts import *
from buttons.stud_buts import socnet_buts, departments_buts
from db.db import get_qeust_from_user, add_qeust

#создание диспатчера
add_rout = Router()

@add_rout.callback_query(F.data =="abb_mod")
@add_rout.message(Command('abb'))
async def main_stud(query: types.Message | types.CallbackQuery):
    if isinstance(query, types.Message):
        # Это команда
        message = query
    else:
        # Это callback-запрос
        message = query.message

    await message.answer(text='Привет аббитуриент\nРадоваться рано,ты еще не поступил.',
                                  reply_markup=main_abb_buts.as_markup())
    await message.delete()


#вывод соцсетей
@add_rout.callback_query(F.data == "soc_net_abb")
async def soc_net_abb(callback: types.CallbackQuery):
    await callback.message.answer(text='Социальные сети:',
                                  reply_markup=socnet_abb_buts.as_markup(resize_keyboard=True))
    await callback.message.delete()

#вопрос
@add_rout.callback_query(F.data == "ask_quest")
async def quest(callback: types.CallbackQuery):
    await callback.message.answer(text='Привет !\n'
                                       'Хочешь задать вопрос или посмотреть свои вопросы?',
                                  reply_markup=quest_buts.as_markup(resize_keyboard=True))
    await callback.message.delete()
################заданные вопросы################
@add_rout.callback_query(F.data == "questions")
async def questions(callback: types.CallbackQuery):
    all_ = await get_qeust_from_user(callback.from_user.id)
    slvd = await get_qeust_from_user(callback.from_user.id,'slvd')
    unslvd = await get_qeust_from_user(callback.from_user.id, 'unslvd')
    if all_:
        await callback.message.answer(text=f'У вас {len(all_)} вопросов\n'
                                           f'Решенных : {len(slvd)}\n'
                                           f'Не решенных : {len(unslvd)}\n\n'
                                           'Какие вопросы хотите вывести?',
                                      reply_markup=questions_.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='У вас нет вопросов(',
                                      reply_markup=not_quests.as_markup(resize_keyboard=True))
    await callback.message.delete()

@add_rout.callback_query(F.data == "solved_quest")
async def solved_quest(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id,'slvd')
    if quests!=[]:
        for quest in quests:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}\n"
                                               f"Ответ: \n {quest['answer']}\n")
        await callback.message.answer(text='Готово!',
                                      reply_markup=not_quests.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='Решенных вопросов нет!',
                                      reply_markup=not_quests.as_markup(resize_keyboard=True))
    await callback.message.delete()
@add_rout.callback_query(F.data == "unsolved_quest")
async def unsolved_quest(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id, 'unslvd')
    if quests:
        for quest in quests:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}")
        await callback.message.answer(text='Готово!',
                                      reply_markup=not_quests.as_markup(resize_keyboard=True))
    else:
        await callback.message.answer(text='Не решенных вопросов нет!',
                                      reply_markup=not_quests.as_markup(resize_keyboard=True))
    await callback.message.delete()

@add_rout.callback_query(F.data == "all_quest")
async def all_quest(callback: types.CallbackQuery):
    quests = await get_qeust_from_user(callback.from_user.id)
    for quest in quests:
        if quest['resolved']:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}\n"
                                               f"Ответ: \n {quest['answer']}\n")
        else:
            await callback.message.answer(text=f"Вопрос:\n {quest['text']}")
    await callback.message.answer(text='Готово!',
                                  reply_markup=not_quests.as_markup(resize_keyboard=True))
    await callback.message.delete()

################заданные вопросы################

################задать вопрос################

class add_quest_(StatesGroup):
    text = State()
@add_rout.callback_query(StateFilter(None),F.data == "add_quest")
async def add_quest(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста напишие текст вашего запроса!\n'
                                       'Текст не должен быть больше 300 символов,\n'
                                       'А также не нужен содержать нецензурную лексику.',
                                  reply_markup=not_quests.as_markup(resize_keyboard=True))
    await state.set_state(add_quest_.text)

@add_rout.message(add_quest_.text,F.text)
async def add_text_q(message: Message, state: FSMContext):
    text = message.text.lower()
    if len(text)>300:
        await message.answer(text='Текст будет обрезаан до 300 символов.')
        text = text[:300]
    await message.answer(text='Текст принят ,ожидайте ответа!',
                         reply_markup=not_quests.as_markup(resize_keyboard=True))
    await add_qeust(message.from_user.id,text)

    await state.clear()
################задать вопрос################



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