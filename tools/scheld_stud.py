import aiohttp
import asyncio
from datetime import date

"""
структура дня
{
  "info": {
    "name": "среда",
    "type": 2,
    "date": "2024-03-06T00:00:00.000Z",
    "parity": 1,
    "weekNumber": 5,
    "dateStr": "06.03.2024"
  },
  "lessons": [
    {
      "number": 1,
      "startAt": "2024-03-06T05:30:00.000Z",
      "time": "08:30-11:40",
      "originalTimeTitle": "1. 08:30-...4ч",
      "parity": 1,
      "range": [3,5,7,9,15],
      "rangeDist": [],
      "lessonName": "Физика (Ф)",
      "type": 4,
      "isStream": false,
      "duration": 4,
      "durationMinutes": 190,
      "isDivision": false,
      "auditoryName": "А-415",
      "teacherName": "доц. Огнева ОФ",
      "isDistant": false,
      "endAt": "2024-03-06T08:40:00.000Z"
    },
    {
      "number": 5,
      "startAt": "2024-03-06T12:40:00.000Z",
      "time": "15:40-19:00",
      "originalTimeTitle": "6. 15:40-...4ч",
      "parity": 1,
      "range": [3,5,7,9,11,15,17],
      "rangeDist": [],
      "lessonName": "Иностранный язык (английский)",
      "type": 4,
      "isStream": true,
      "duration": 4,
      "durationMinutes": 200,
      "isDivision": false,
      "auditoryName": "Г-905 Г-912",
      "teacherName": null,
      "subInfo": "аудитории 7-го этажа",
      "isDistant": false,
      "endAt": "2024-03-06T16:00:00.000Z"
    }
  ]
}
"""

async def get_scheld(group):
    """
    асинхронно отправляет запрос к апи с группой,возвращает словарь
    :param group: группа для которой нужно получить расписание
    :return: словарь с расписанием
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://parser.ystuty.ru/api/ystu/schedule/group/{group}") as response:
            return await response.json()
async def scheld_week(group):
    """
    асинхронно из полученного словаря получает расписание на эту неделю по группе
    :param group:группа к каторой поучаю расписание
    :return: словарь расписание на эту неделю,если распиания нет то None
    """
    try:
        t = await get_scheld(group)
        for j in range(len(t['items'])):
            for i in range(len(t['items'][j]['days'])):
                dt = (t['items'][j]['days'][i]['info']['date']).split("T")[0]
                res=0
                if dt == str(date.today()):
                    res =t['items'][j]['days']
                    break
            if res!=0:
                break
        return res
    except :
        return None

async def scheld_next_week(group):
    """
    асинхронно из полученного словаря получает расписание на следующую неделю по группе
    :param group:группа к каторой поучаю расписание
    :return:словарь расписание на следующую неделю,если распиания нет то None
    """
    try:
        t = await get_scheld(group)
        for j in range(len(t['items'])):
            for i in range(len(t['items'][j]['days'])):
                dt = (t['items'][j]['days'][i]['info']['date']).split("T")[0]
                res=0
                if dt == str(date.today()):
                    res =t['items'][j+1]['days']
                    break
            if res!=0:
                break
        return res
    except :
        return None

async def scheld_today(group):
    """
    асинхронно из полученного словаря получает расписание на сегодня по группе
    :param group:группа к каторой получает расписание
    :return: словарь расписание на сегодня,если распиания нет то None
    """
    try:
        t = await get_scheld(group)
        for j in range(len(t['items'])):
            for i in range(len(t['items'][j]['days'])):
                dt = (t['items'][j]['days'][i]['info']['date']).split("T")[0]
                res=0
                if dt == str(date.today()):
                    res =t['items'][j]['days'][i]
                    break
            if res!=0:
                break
        return res
    except :
        return None

async def scheld_tomorrow(group):
    """
    асинхронно из полученного словаря получает расписание на завтра по группе
    :param group:группа к каторой получает расписание
    :return: словарь расписание на завтра,если распиания нет то None
    """
    try:
        t = await get_scheld(group)
        for j in range(len(t['items'])):
            for i in range(len(t['items'][j]['days'])):
                dt = (t['items'][j]['days'][i]['info']['date']).split("T")[0]
                res=0
                if dt == str(date.today()):
                    res =t['items'][j]['days'][i+1]
                    break
            if res!=0:
                break
        return res
    except :
        return None

#для тестировки функций ,при отправьке на гит закоменьтить
# async def main():
#     t3 = await scheld_today('цис-16')
#     print(t3)
# asyncio.run(main())