import aiohttp
import asyncio

async def get_groups_instit():
    """
    асинхронно отправляет запрос к апи с группой,возвращает словарь
    :param group: группа для которой нужно получить расписание
    :return: словарь с расписанием
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://parser.ystuty.ru/api/ystu/schedule/institutes") as response:
            return await response.json()

async def groups():
    try:
        t = await get_groups_instit()
        t=t['items']
        res=[]
        for i in t:
            res.extend(i['groups'])
        res = [i.lower() for i in res]
        return res
    except :
        return None

# #для тестировки функций ,при отправьке на гит закоменьтить
# async def main():
#     print(await groups())
# asyncio.run(main())