# ystu-bot
Студенческий проект по разработке полезного телеграмм ботя для вуза ЯГТУ.
---------------------------------------------------------------------------
Наш бот возможно не лучший, но уже и не "hello world!"      
Разработка ведеться студентами первого курса,поэтому не судите строго.      
Всё чего нам не ххвотаем мы запиливаем здесь ,чтобы нам же было удобно.     

Скоро будет доделан.        

_________________________________
# Техническая информация      
Структура:   
main - основной файл для запуска бота   
amvera.yml - файл для запуска в amvera    
app.log - логи приложения\
db_y2.backup - дамп базы данных\
properties - файл с глобальными переменными используемых в приложении\
requirements - используемые технологии\
buttons - кнопки которые используются в диспатчерах,содержит:   
--- abb_buts - кнопки для бота для абитуриентов     
--- stud_buts - кнопки для бота для студентов   
--- other_buts - кнопки для единичных диспатчеров,не отнесенных не к какой группе   
handlers - диспатчеры для обработки кнопок,команд в ботах,содержит:     
--- abb_hand - обработчики для бота для абитуриентов        
--- stud_hand - обработчики для бота для студентов      
--- other_hand - обработчики для единичных диспатчеров,не отнесенных не к какой группе     
db - файл с запросами к базе данных     
tools - инструменты для взаимосвязи со стороннми сервисами      
--- lists - дает возможность получить список групп      
--- sheld_stud - получение и распаковка расписания для студентов 
--- notif - автоматическая отправка расписания по времени 

Запуск осуществляется запуском main.py

Используется:       
aiogram 3.x     
aiohttp     
asyncio     
asyncpg(PostgreSQL)     
