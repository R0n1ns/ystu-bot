import asyncio
from aiogram import Bot, Dispatcher,types
import logging
import os
#импорт отдельных диспатчеров
from handlers.stud_hand import us_rout
from handlers.abb_hand import add_rout
from handlers.other_hand import oth_rout
from properties import token
from tools.notif import notify

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher()

#подключение отдельных диспатчеров
dp.include_router(us_rout)
dp.include_router(add_rout)
dp.include_router(oth_rout)

# Запуск процесса поллинга новых апдейтов
async def main():
    polling_task = asyncio.Task(dp.start_polling(bot))
    my_async_function_task = asyncio.Task(notify(bot))

    await asyncio.gather(polling_task, my_async_function_task)


if __name__ == "__main__":
    asyncio.run(main())


