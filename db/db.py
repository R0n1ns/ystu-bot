import asyncpg
import asyncio

# host = 'ystu.czksg02uc9h6.eu-north-1.rds.amazonaws.com'
# port = '5432'
# database = 'ystu'
# user = 'postgres'
# pas = 'avrora_123'

host = 'localhost'
port = '5432'
database = 'ystu_bot'
user = 'postgres'
pas = '0725'

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
async def if_fav_stud(id_tg):
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
    if req == 'None':
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
    :param fav_group: None или фаворитная группа
    """
    id_tg = str(id_tg)
    await async_db_request(f"UPDATE students SET fav = '{fav_group}' WHERE id_tg = '{id_tg}';", params=None)
############ ФАВАРИТНАЯ ГРУППА ############

############ УЧИТЕЛЬ ############
async def teach_add_tg_id(number,id_tg):
    """
    добавляет телеграмм id к сущ записи с номером телефона
    :param number:
    :param id_tg:
    :return:
    """
    await async_db_request(f"UPDATE teachers SET tg_id = '{id_tg}' WHERE phone_number  = '{number}';", params=None)


async def teach_if(number):
    """
    ищет запись об учителе в базе
    :param number:
    :return:
    """
    req = await async_db_request(f"SELECT * FROM teachers WHERE phone_number  = '{number}';",params=None)
    if req ==[]:
        return False
    else:
        return True

async def teach_if_id(id):
    """
    ищет запись об учителе в базе по id
    :param id:
    :return:
    """
    req = await async_db_request(f"SELECT * FROM teachers WHERE tg_id  = '{id}';",params=None)
    if req ==[]:
        return False
    else:
        return True
############ УЧИТЕЛЬ ############

############ АББИТУРИЕНТ ############

############ АББИТУРИЕНТ ############
# async def main():
#     print(await replace_fav_stud(824555006,'No'))
#
# asyncio.run(main())


#удалить все из таблицы TRUNCATE TABLE table_name;