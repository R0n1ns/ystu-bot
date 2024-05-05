import asyncio
import logging

from db.db import evd_notif, evd_notif_upd, evd_notif_send, evw_notif, evw_notif_send, evw_notif_upd, evl_notif, \
    evl_notif_upd, evl_notif_send, if_notif
from tools.scheld_stud import scheld_today, scheld_week

from datetime import datetime
from properties import evd_time, evw_time, evl_time_schem, p

# #переробатывает время в секунды
evl_time = [i[0]*3600 + i[1]*60 for i in evl_time_schem]#время отправки уведомлений перед парами
evl_time = [[evl_time[i],evl_time_schem[i][2]] for i in range(0,len(evl_time))] # [[14400, '8:30'], [24000, '10:10'], [30000, '12:20'], [37800, '14:00'], [43800, '15:40'], [49800, '17:10'], [55800, '19:00']]

###################################

#################  сообщения каждую пару #########################
async def evl_sch():
    users =await evl_notif()
    for user in users:
        sch = await scheld_today(user['group'])
        lessons_ = {}
        if not((sch ==0) or (sch == None)):
            for i in sch['lessons']:
                text ="следующая пара : \n" +f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n"
                time = i['originalTimeTitle'].split("-")[0].split(" ")[1]
                lessons_[time] = text
        else:
            u = await if_notif(user[0])
            if not(u[1]):
                lessons_ = {"8:30":"на расслабоне🎆"}
        await evl_notif_upd(user['id_tg'], str(lessons_).replace("'",'"'))
async def evl(bot):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p*3600
    for i in evl_time:
        time_next =  abs(i[0] - time)
        await asyncio.sleep(time_next)
        users = await evl_notif_send()
        logging.info(f"Отправлено на пару в {i[1]} уведомлений {len(users)}")
        for user in users:
            text = dict(eval(user["l_sch"]))
            if i[1] in text.keys():
                text =text[i[1]]
                #print(user["id_tg"], text)
                await bot.send_message(user["id_tg"], text)
##################################################################

################# ежедневные сообщения #########################
async def evd_sch():
    users =await evd_notif()
    for user in users:
        sch = await scheld_today(user['group'])
        if not((sch ==0) or (sch == None)):
            lessons = "".join([
                                  f"{i['originalTimeTitle']} | {i['lessonName']}\n{i['auditoryName']} | {'Неизвестно' if i['teacherName'] is None else i['teacherName']}\n"
                                  for i in sch['lessons']])
            sch_ = f"{sch['info']['name']}\nПары на день:\n" + lessons
        else:
            sch_ = "на расслабоне🎆"
        await evd_notif_upd(user['id_tg'], sch_)

async def evd(bot):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p*3600
    time_next = abs(evd_time*3600 - time)
    await asyncio.sleep(time_next)
    users = await evd_notif_send()
    logging.info(f"Отправлено ежедневных уведомлений {len(users)}")
    for user in users:
        #print(user["id_tg"], user["d_sch"])
        await bot.send_message(user["id_tg"], user["d_sch"])
#############################################################

################# еженедельные сообщения ####################
async def evw_sch():
    users = await evw_notif()
    for user in users:
        sch = await scheld_week(user['group'])
        if not((sch ==0) or (sch == None)):
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
async def evw(bot):
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p*3600
    time_next = abs(evw_time*3600 - time)
    await asyncio.sleep(time_next)
    users = await evw_notif_send()
    logging.info(f"Отправлено еженедельных уведомлений {len(users)}")
    for user in users:
        # print(user["id_tg"], user["w_sch"])
        await bot.send_message(user["id_tg"], user["w_sch"])
#############################################################


async def notify(bot):
    time_w =  datetime.today().weekday()
    time = datetime.now()
    time = time.second + time.minute * 60 + time.hour * 3600 + p*3600
    next_time = 24*3600 + 30*60 - time
    logging.info(f"След. время обновления расписания через {next_time/3600}")
    await asyncio.sleep(next_time)
    #ежедневные уведомления
    await evd_sch()
    await evd(bot)
    # каждую пару уведомления
    await evl_sch()
    await evl(bot)
    #еженедельное уведомлени
    if time_w == 1:
        await evw_sch()
        await evw(bot)
    logging.info(f"Уведомления успешно отправлены")
    #заново
    await asyncio.sleep(300)
    await notify(bot)

# async def main():
# if __name__ == "__main__":
#     asyncio.run(main())



