import asyncpg
import asyncio

host = 'ystu.czksg02uc9h6.eu-north-1.rds.amazonaws.com'
port = '5432'
database = 'ystu'
user = 'ystu'
pas = 'avrora_123'

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



async def new_review(rev,them,who):
    """
    добавляет новый отзыв в базу данных
    :param rev: сам отзыв
    :param them: тема отзыва
    :param who: кто отправил отзыв
    """
    await async_db_request(f"INSERT INTO reviews (review,theme,who_send) VALUES ('{rev}','{them}','{who}');",params=None)


# async def main():
#     await new_review('wrerwe','erwerrwe',1231231)
#
# asyncio.run(main())


#удалить все из таблицы TRUNCATE TABLE table_name;