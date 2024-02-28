import asyncio
from aiogram import types,Router
from aiogram.filters.command import Command
#импорт кнопок
from buttons.abb_buts import *
#создание диспатчера
add_rout = Router()