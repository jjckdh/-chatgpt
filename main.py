from message import Aligenie
from message import AliGenieFrida
import asyncio


from Chat import Chat  # Chat文件中的Chat类
import datetime
import time


last_timestamp = int(time.time())


async def print_every_two_seconds():
    while True:
        aliGenieFrida = AliGenieFrida()
        qa = aliGenieFrida.get_data
        query = qa['query']
        reply = qa['reply']
        queryTime = qa['queryTime']
        last = int(time.mktime(datetime.datetime.strptime(queryTime, '%Y-%m-%d %H:%M:%S.%f').timetuple()))
        global last_timestamp
        print(last_timestamp, query, last)
        if query != '' and last > last_timestamp:
            last_timestamp = last
            # 前面的代码是用于获取天猫精灵的对话记录，可以不用看，主要是Chat类中的方法
            # 将获取的提问导入chat类中的方法中，chat使用爬虫技术来获取chatgpt的回答
            message = [{'role': 'user', 'content': query}, ]  # message为发出的问题

            content = Chat.two(message)  # content来自completion = {'role': '', 'content': ''}

            print(f"问题：{query}，天猫精灵的回答：{reply}，chat的回答：{content}")
            Aligenie.push_message(content)
        await asyncio.sleep(2)


async def main():
    task = asyncio.create_task(print_every_two_seconds())
    await task


if __name__ == '__main__':
    asyncio.run(main())