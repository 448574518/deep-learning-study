import nonebot
from nonebot import on_command, CommandSession
import requests
import json


@on_command('sexy', aliases={"来张色图", "来张涩图", "涩图", "涩涩"})
async def get_a_setu(session: CommandSession):
    # await session.send("找图中，稍等")
    params = {
        "r18": "0"  # 0为非r18，1为r18，2为混合
    }
    url = "https://api.lolicon.app/setu/v2"
    response = requests.get(url, params)
    response = json.loads(response.text)
    data = (response['data'])[0]
    urls = data['urls']
    setu_url = urls['original']
    groupid = session.event.group_id
    bot = nonebot.get_bot()
    CQ_msg = r'[CQ:image,' r'file=' + str(setu_url) + r']'
    await bot.send_group_msg(group_id=groupid, message=CQ_msg)
