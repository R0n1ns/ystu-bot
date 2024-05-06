import asyncpg
from properties import host,port,database,user,pas


############ ОБЩЕЕ ############
async def async_db_request(query, params):
  """
  Асинхронная функция для выполнения запроса к базе данных postgresql
  Args:
      query: Текст запроса
      params: Словарь с параметрами запроса
  Returns:
      Результат запроса
  """
  conn = await asyncpg.connect(
      database=database,
      user=user,
      password=pas,
      host=host,
      port=port)
  try:
    if params is None:
      result = await conn.fetch(query)
    else:
      result = await conn.fetch(query, params)
  except Exception as e:
    raise RuntimeError(f"Ошибка при запросе к базе данных: {e}")
  finally:
    await conn.close()
  return result
############ ОБЩЕЕ ############
async def new_stud(tg_id):
    """
    добавляет нового пользователя
    :param tg_id: id пользователя
    """
    await async_db_request(f"INSERT INTO students (id_tg) VALUES ({tg_id});",params=None)
############ ОТЗЫВЫ ############

############ ОТЗЫВЫ ############
async def new_review(rev,them,who):
    """
    добавляет новый отзыв в базу данных
    :param rev: сам отзыв
    :param them: тема отзыва
    :param who: кто отправил отзыв
    """
    await async_db_request(f"INSERT INTO reviews (review,theme,who_send) VALUES ('{rev}','{them}','{who}');",params=None)
############ ОТЗЫВЫ ############

############ ФАВАРИТНАЯ ГРУППА ############
async def if_fav_stud(id_tg,group="None"):
    """
    Возвращает True если фав группа есть,если нет то False
    :param id_tg: тг id пользователя
    :return: bool
    """
    id_tg = str(id_tg)
    req = await async_db_request(f"SELECT fav FROM students WHERE id_tg = '{id_tg}';",params=None)
    if req == []:
        await new_stud(id_tg)
        return False
    req = req[0]['fav']
    if req == 'None' or req =='No':
        return False
    else:
        return req


async def add_fav_stud(id_tg,fav_group):
    """
    Добавляет фаворитную группу студенту
    если записи о студенте нет, то добовляет студента и группу и возвращает True
    если студент есть ,а группы нет, то дополняет группу и возращает True
    :param id_tg: телеграмм id пользвоателя
    :param fav_group: фаворитная группа
    """
    id_tg = str(id_tg)
    req = await async_db_request(f"SELECT id_tg FROM students WHERE id_tg = '{id_tg}';",params=None)
    #req = await async_db_request(f"SELECT fav_scheld FROM students WHERE id_tg = '{id_tg}';",params=None)
    if req == []:
        await async_db_request(f"INSERT INTO students (id_tg,fav) VALUES ('{id_tg}','{fav_group}')", params=None)
        return True
    else:
        fav = await async_db_request(f"SELECT fav FROM students WHERE id_tg = '{id_tg}';", params=None)
        fav = fav[0]['fav']
        if fav == 'None':
            await async_db_request(f"UPDATE students SET fav = '{fav_group}' WHERE id_tg = '{id_tg}';", params=None)
            return True
        else:
            return fav
async def replace_fav_stud(id_tg,fav_group):
    """
    Изменяет фаворитную группу на новую или удаляет ее
    Если fav_group == None,то fav_group = 'None'
    Если чтото другое ,то обновляет группу
    :param id_tg: телеграмм id пользвоателя
    :param fav_group: None или фаворитная группа DELETE \"group\" FROM notif WHERE id_tg = '{id_tg}';
    """
    id_tg = str(id_tg)
    # await async_db_request(f"UPDATE notif SET \"group\" = '{fav_group}' WHERE id_tg = '{id_tg}';", params=None)
    await async_db_request(f"UPDATE students SET fav = '{fav_group}' WHERE id_tg = '{id_tg}';", params=None)
    if fav_group == None:
        await async_db_request(f"UPDATE notif SET evd=false WHERE id_tg = '{id}';", params=None )
        await async_db_request(f"UPDATE notif SET evw=false WHERE id_tg = '{id}';", params=None)
        await async_db_request(f"UPDATE notif SET evl=false WHERE id_tg = '{id}';", params=None)
############ ФАВАРИТНАЯ ГРУППА ############

############ вапросы ############
async def add_qeust(id,text):
    """
    добавляет вопрос
    :param id: телеграмм id
    :param text: максимум 300 символов
    """
    id = str(id)
    await async_db_request(f"INSERT INTO questions (id_tg, text) VALUES ('{id}', '{text}');", params=None)

async def get_qeust_from_user(id,type='all'):
    """
    Отправляет заданные вопросы пользователя
    :param type: тип вопросов slvd,unslvd,all
    :param id: id пользователя
    :return: список вопросов пользователя
    """
    id = str(id)
    if type=='all':
        return await async_db_request(f"SELECT text,resolved,answer FROM public.questions WHERE id_tg='{id}';", params=None)
    elif type=='slvd':
        return await async_db_request(f"SELECT text,answer FROM public.questions WHERE id_tg = '{id}' AND resolved = True;", params=None)
    elif type=='unslvd':
        return await async_db_request(f"SELECT text,answer FROM public.questions WHERE id_tg = '{id}' AND resolved = False;", params=None)

async def get_all_act_qeust():
    """
    возвращает все нерешенные вопросы
    :return: все нерешенные вопросы
    """
    return await async_db_request(f"SELECT id_quest,id_tg,text FROM public.questions WHERE resolved=false;", params=None)


############ вапросы ############



############ уведомления ############
async def if_notif(id,group='None'):
    user = await async_db_request(f'SELECT evw,evd,evl FROM notif where id_tg = \'{id}\';', params=None)
    if user ==[]:
        await async_db_request(f'INSERT INTO notif(id_tg,"group") VALUES  (\'{id}\',\'{group}\');', params=None)
        return[False,False,False]
    else:
        return [user[0][0],user[0][1],user[0][2]]
#каждый день#
async def swith_evd(id,sw):
    if sw == 'on':
        await async_db_request(f"UPDATE notif SET evd=true WHERE id_tg = '{id}';", params=None)
    elif sw == 'off':
        await async_db_request(f"UPDATE notif SET evd=false WHERE id_tg = '{id}';", params=None )
async def evd_notif():
    users = await async_db_request(f'SELECT id_tg, "group" FROM notif where evd =true; ', params=None)
    return users

async def evd_notif_upd(id,sch):
    await async_db_request(f"UPDATE notif SET d_sch = '{sch}' WHERE id_tg = '{id}';", params=None)

async def evd_notif_send():
    users = await async_db_request(f'SELECT id_tg, d_sch FROM notif where evd =true; ', params=None)
    return users

#каждую неделю#
async def swith_evw(id,sw):
    if sw == 'on':
        await async_db_request(f"UPDATE notif SET evw=true WHERE id_tg = '{id}';", params=None)
    elif sw == 'off':
        await async_db_request(f"UPDATE notif SET evw=false WHERE id_tg = '{id}';", params=None)
async def evw_notif():
    users = await async_db_request(f'SELECT id_tg, "group" FROM notif where evw =true; ', params=None)
    return users

async def evw_notif_upd(id,sch):
    await async_db_request(f"UPDATE notif SET w_sch = '{sch}' WHERE id_tg = '{id}';", params=None)

async def evw_notif_send():
    users = await async_db_request(f'SELECT id_tg, w_sch FROM notif where evw =true;', params=None)
    return users
#каждую пару#
async def swith_evl(id,sw):
    if sw == 'on':
        await async_db_request(f"UPDATE notif SET evl=true WHERE id_tg = '{id}';", params=None)
    elif sw == 'off':
        await async_db_request(f"UPDATE notif SET evl=false WHERE id_tg = '{id}';", params=None)
async def evl_notif():
    users = await async_db_request(f'SELECT id_tg, "group" FROM notif where evl =true; ', params=None)
    return users

async def evl_notif_upd(id,sch):
    await async_db_request(f"UPDATE notif SET l_sch = '{sch}' WHERE id_tg = '{id}';", params=None)

async def evl_notif_send():
    users = await async_db_request(f'SELECT id_tg, l_sch FROM notif where evl =true;', params=None)
    return users
############ уведомления ############


############ УЧИТЕЛЬ ############

############ АББИТУРИЕНТ ############
#
############ АББИТУРИЕНТ ############
# async def main():
#     print(await if_notif("824555006"))
#     await swith_evw("824555006",'off')
#     print(await if_notif("824555006"))
# asyncio.run(main())


#удалить все из таблицы TRUNCATE TABLE table_name;