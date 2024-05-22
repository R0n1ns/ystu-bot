from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

#кнопка основного меню аббитуриента
main_abb_=[["Направления обучения","majors"],["Задать вопрос","ask_quest"],["Соц. сети","soc_net_abb"],["Новости","news"],["Приёмная комиссия","committee"]]
#инциаизация клавиатуры
main_abb_buts = InlineKeyboardBuilder()
#генерация клавиатуры
for i in main_abb_:
    main_abb_buts.row(InlineKeyboardButton(text=i[0], callback_data=i[1]))


#инциаизация клавиатуры
socnet_abb_buts = InlineKeyboardBuilder()
#генерация клавиатуры
socnet_abb_buts.row(InlineKeyboardButton(text='Новости',callback_data='news_abb'))
socnet_abb_buts.row(InlineKeyboardButton(text='Кафедры',callback_data='departments_abb'))
socnet_abb_buts.row(InlineKeyboardButton(text='Институты',callback_data='institutes_abb'))
socnet_abb_buts.row(InlineKeyboardButton(text='В меню абитуриента', callback_data='abb_mod'))


news_abb_buts = InlineKeyboardBuilder()
news_abb_buts.row(InlineKeyboardButton(text='ВКонтакте',url='https://vk.com/ystu'))
news_abb_buts.row(InlineKeyboardButton(text='Telegram',url='https://t.me/YaroslavlSTU'))
news_abb_buts.row(InlineKeyboardButton(text='Назад', callback_data='abb_mod'))
news_abb_buts.add(InlineKeyboardButton(text='В меню абитуриента', callback_data='abb_mod'))

#инциаизация клавиатуры
departments_abb_buts = InlineKeyboardBuilder()
#генерация клabb_авиатуры
departments_abb_buts.row(InlineKeyboardButton(text='Высшей математики', url='https://vk.com/ystu'))
departments_abb_buts.row(InlineKeyboardButton(text='Физики',url='https://ссылки.нет'))
departments_abb_buts.row(InlineKeyboardButton(text='Физическое воспитание',url='https://vk.com/ystu_physedu'))
departments_abb_buts.row(InlineKeyboardButton(text='Экономики и управления',url='https://vk.com/eyystu'))
departments_abb_buts.row(InlineKeyboardButton(text='Иностранных языков',url='https://vk.com/ystuforlang'))
departments_abb_buts.row(InlineKeyboardButton(text='Назад', callback_data='soc_net_abb'))
departments_abb_buts.add(InlineKeyboardButton(text='В меню абитуриента', callback_data='abb_mod'))

#Инcтитуты
institutes_abb_buts = InlineKeyboardBuilder()
institutes_abb_buts.row(InlineKeyboardButton(text='Цифровых систем', url='https://vk.com/ist_ystu'))
institutes_abb_buts.row(InlineKeyboardButton(text='Экономики и менеджмента ',url='https://vk.com/ief_ystu'))
institutes_abb_buts.row(InlineKeyboardButton(text='Инженеров строительства и транспорта',url='https://vk.com/iisitystu'))
institutes_abb_buts.row(InlineKeyboardButton(text='Инженерии и машиностроения',url='https://ссылки.нет'))
institutes_abb_buts.row(InlineKeyboardButton(text='Архитектуры и дизайна',url='https://ссылки.нет'))
institutes_abb_buts.row(InlineKeyboardButton(text='Химии и химической технологии',url='https://vk.com/public218972913'))
institutes_abb_buts.row(InlineKeyboardButton(text='Назад', callback_data='soc_net_abb'))
institutes_abb_buts.add(InlineKeyboardButton(text='В меню абитуриента', callback_data='abb_mod'))

#вопросы
quest_buts = InlineKeyboardBuilder()
quest_buts.row(InlineKeyboardButton(text='Задать вопрос', callback_data='add_quest'))
quest_buts.row(InlineKeyboardButton(text='Заданные вопросы',callback_data='questions'))

#questions
questions_ = InlineKeyboardBuilder()
questions_.row(InlineKeyboardButton(text='Решенные', callback_data='solved_quest'))
questions_.row(InlineKeyboardButton(text='Не решенные', callback_data='unsolved_quest'))
questions_.row(InlineKeyboardButton(text='Все', callback_data='all_quest'))
questions_.row(InlineKeyboardButton(text='В меню', callback_data='abb_mod'))

#not quests
not_quests = InlineKeyboardBuilder()
not_quests.row(InlineKeyboardButton(text='Назад', callback_data='ask_quest'))
not_quests.row(InlineKeyboardButton(text='В меню', callback_data='abb_mod'))

#Направления обучения
majors_buts = InlineKeyboardBuilder()
majors_buts.add(InlineKeyboardButton(text='В меню абитуриента', callback_data='abb_mod'))