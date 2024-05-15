import asyncio
import logging
from datetime import datetime, timedelta

from db.db import evd_notif, evd_notif_upd, evd_notif_send, evw_notif, evw_notif_send, evw_notif_upd, evl_notif, evl_notif_upd, evl_notif_send, if_notif
from tools.scheld_stud import scheld_today, scheld_week
from properties import evd_time, evw_time, evl_time_schem, p, token

# Перерабатывает время в секунды
evl_time = [i[0]*3600 + i[1]*60 for i in evl_time_schem]
evl_time = [[evl_time[i], evl_time_schem[i][2]] for i in range(len(evl_time))]

async def evl_sch():
    users = await evl_notif()
    for user in users:
        sch = await scheld_today(user['group'])
        lessons_ = {}
        if sch and sch != 0:
            for i in sch['lessons']:
                text = f"следующая пара:\n{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n"
                time = i['originalTimeTitle'].split("-")[0].split(" ")[1]
                lessons_[time] = text
        else:
            u = await if_notif(user[0])
            if not u[1]:
                lessons_ = {"8:30": "на расслабоне🎆"}
        await evl_notif_upd(user['id_tg'], str(lessons_).replace("'", '"'))

async def evl(bot, tst=False):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p * 3600
    for i in evl_time:
        time_next = abs(i[0] - time)
        if bot is None:
            print("evl -- ", time_next)
            time_next = 10
        if tst:
            logging.info(f"----Отправка ежепарных уведомлений через {time_next}")
        await asyncio.sleep(time_next)
        users = await evl_notif_send()
        logging.info(f"Отправлено на пару в {i[1]} уведомлений {len(users)}")
        for user in users:
            text = dict(eval(user["l_sch"]))
            if i[1] in text.keys():
                text = text[i[1]]
                if bot is None:
                    print(user["id_tg"], text)
                else:
                    await bot.send_message(user["id_tg"], text)

async def evd_sch():
    users = await evd_notif()
    for user in users:
        sch = await scheld_today(user['group'])
        if sch and sch != 0:
            lessons = "".join([
                f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n"
                for i in sch['lessons']])
            sch_ = f"{sch['info']['name']}\nПары на день:\n" + lessons
        else:
            sch_ = "на расслабоне🎆"
        await evd_notif_upd(user['id_tg'], sch_)

async def evd(bot, tst=False):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p * 3600
    time_next = abs(evd_time * 3600 - time)
    if bot is None:
        print("evd -- ", time_next)
        time_next = 10
    if tst:
        logging.info(f"----Отправка ежедневных уведомлений через {time_next}")
    await asyncio.sleep(time_next)
    users = await evd_notif_send()
    logging.info(f"Отправлено ежедневных уведомлений {len(users)}")
    for user in users:
        if bot is None:
            print(user["id_tg"], user["d_sch"])
        else:
            await bot.send_message(user["id_tg"], user["d_sch"])

async def evw_sch():
    users = await evw_notif()
    for user in users:
        sch = await scheld_week(user['group'])
        if sch and sch != 0:
            res = []
            for j in sch:
                lessons = "".join([
                    f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n"
                    for i in j['lessons']])
                k = f"{j['info']['name']}\nПары на день:\n" + lessons
                res.append(k)
            sch_ = "".join(res)
        else:
            sch_ = "на расслабоне🎆"
        await evw_notif_upd(user['id_tg'], sch_)

async def evw(bot, tst=False):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p * 3600
    time_next = abs(evw_time * 3600 - time)
    if bot is None:
        print("evw -- ", time_next)
        time_next = 10
    await asyncio.sleep(time_next)
    users = await evw_notif_send()
    logging.info(f"Отправлено еженедельных уведомлений {len(users)}")
    for user in users:
        if bot is None:
            print(user["id_tg"], user["w_sch"])
        else:
            await bot.send_message(user["id_tg"], user["w_sch"])

async def notify(bot, tst=False):
    while True:
        time_w = datetime.today().weekday()
        time = datetime.now()
        time = time.second + time.minute * 60 + time.hour * 3600 + p * 3600
        next_time = 24 * 3600 + 30 * 60 - time
        if bot is None:
            print(f"След. время обновления расписания через {next_time / 3600}")
            next_time = 10
        logging.info(f"След. время обновления расписания через {next_time / 3600}")
        await asyncio.sleep(next_time)
        if bot is None:
            print("Данные обновлены")
        await evd_sch()
        await evl_sch()
        if tst:
            logging.info("----Данные обновлены")
        d = asyncio.create_task(evd(bot, tst))
        l = asyncio.create_task(evl(bot, tst))
        tasks = [d, l]
        if time_w == 0:
            await evw_sch()
            w = asyncio.create_task(evw(bot, tst))
            tasks.append(w)
        await asyncio.gather(*tasks)
        logging.info("Уведомления успешно отправлены")
        if bot is None:
            print("Заново")
        await asyncio.sleep(300)


