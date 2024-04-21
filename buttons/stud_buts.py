from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup ,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder ,ReplyKeyboardBuilder

#кнопка основного меню студента
main_stud_=[["Расписание","scheld"],["Отзывы","revie"],["Соц сети","soc_net"],["О вузе","news"]]
#инциаизация клавиатуры
main_stud_buts = InlineKeyboardBuilder()
#генерация клавиатуры
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[0][0],callback_data=main_stud_[0][1]))
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[1][0],callback_data=main_stud_[1][1]))
main_stud_buts.row(InlineKeyboardButton(text=main_stud_[2][0],callback_data=main_stud_[2][1]))
main_stud_buts.add(InlineKeyboardButton(text=main_stud_[3][0],callback_data=main_stud_[3][1]))

#кнопка основного выбора даты для рассписания
scheld_date=["Сегодня","Завтра","Эта неделя","Cлед неделя"]
#инциаизация клавиатуры
scheld_date_buts = ReplyKeyboardBuilder()
#генерация клавиатуры
scheld_date_buts.row(KeyboardButton(text=scheld_date[0]))
scheld_date_buts.add(KeyboardButton(text=scheld_date[1]))
scheld_date_buts.row(KeyboardButton(text=scheld_date[2]))
scheld_date_buts.add(KeyboardButton(text=scheld_date[3]))


#кнопка основного выбора даты для рассписания
scheld_buts = InlineKeyboardBuilder()
#генерация клавиатуры
scheld_buts.row(InlineKeyboardButton(text="В главное меню.",callback_data='stud_mod'))



#инциаизация клавиатуры
socnet_buts = InlineKeyboardBuilder()
#генерация клавиатуры
socnet_buts.row(InlineKeyboardButton(text='Новости', callback_data='news'))
socnet_buts.row(InlineKeyboardButton(text='Кафедры',callback_data='departments'))
socnet_buts.row(InlineKeyboardButton(text='Институты',callback_data='institutes'))
socnet_buts.row(InlineKeyboardButton(text='В меню студента', callback_data='stud_mod'))

#Соцсети с новостями
news_buts = InlineKeyboardBuilder()
news_buts.row(InlineKeyboardButton(text='ВКонтакте',url='https://vk.com/ystu'))
news_buts.row(InlineKeyboardButton(text='Telegram',url='https://t.me/YaroslavlSTU'))
news_buts.row(InlineKeyboardButton(text='Назад', callback_data='stud_mod'))
news_buts.add(InlineKeyboardButton(text='В меню студента', callback_data='stud_mod'))

#Кафедры
departments_buts = InlineKeyboardBuilder()
#генерация клавиатуры
departments_buts.row(InlineKeyboardButton(text='Высшей математики', url='https://vk.com/ystu'))
departments_buts.row(InlineKeyboardButton(text='Физики',url='https://ссылки.нет'))
departments_buts.row(InlineKeyboardButton(text='Физическое воспитание',url='https://vk.com/ystu_physedu'))
departments_buts.row(InlineKeyboardButton(text='Экономики и управления',url='https://vk.com/eyystu'))
departments_buts.row(InlineKeyboardButton(text='Иностранных языков',url='https://vk.com/ystuforlang'))
departments_buts.row(InlineKeyboardButton(text='Назад', callback_data='soc_net'))
departments_buts.add(InlineKeyboardButton(text='В меню студента', callback_data='stud_mod'))

#Инcтитуты
institutes_buts = InlineKeyboardBuilder()
institutes_buts.row(InlineKeyboardButton(text='Цифровых систем', url='https://vk.com/ist_ystu'))
institutes_buts.row(InlineKeyboardButton(text='Экономики и менеджмента ',url='https://vk.com/ief_ystu'))
institutes_buts.row(InlineKeyboardButton(text='Инженеров строительства и транспорта',url='https://vk.com/iisitystu'))
institutes_buts.row(InlineKeyboardButton(text='Инженерии и машиностроения',url='https://ссылки.нет'))
institutes_buts.row(InlineKeyboardButton(text='Архитектуры и дизайна',url='https://ссылки.нет'))
institutes_buts.row(InlineKeyboardButton(text='Химии и химической технологии',url='https://vk.com/public218972913'))
institutes_buts.row(InlineKeyboardButton(text='Назад', callback_data='soc_net'))
institutes_buts.add(InlineKeyboardButton(text='В меню студента', callback_data='stud_mod'))

#Фаворитные группы
fav_ = ReplyKeyboardBuilder()
fav_.row(KeyboardButton(text='Да)'))
fav_.add(KeyboardButton(text='Нет('))
