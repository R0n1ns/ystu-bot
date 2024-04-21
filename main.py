import asyncio
from aiogram import Bot, Dispatcher,types
import logging

#импорт отдельных диспатчеров
from handlers.stud_hand import us_rout
from handlers.abb_hand import add_rout
from handlers.other_hand import oth_rout

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="6058267012:AAG5BkwEQNzB52ThgW1DIlb4u_CKP1ZPtYQ")
# Диспетчер
dp = Dispatcher()

#подключение отдельных диспатчеров
dp.include_router(us_rout)
dp.include_router(add_rout)
dp.include_router(oth_rout)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
