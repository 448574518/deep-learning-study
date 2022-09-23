import logging
import random

import nonebot
from nonebot import CommandSession, on_command
from nonebot import NLPSession, on_natural_language, IntentCommand

log = logging.getLogger("__init__")


@on_command("waterB")
async def rep_waterB(session: CommandSession):
    userid = session.event.user_id
    # 如果是源宝
    if str(userid) == "1031316110":
        await session.send("源宝又在水群啊，休息一下好不好")
    # 如果是雪阳
    elif str(userid) == "1658735391":
        await session.send("fw雪阳，天天叫")
    # 如果是鲍
    elif str(userid) == "464180657":
        await session.send("肥逼！")
    # 如果是俩星
    elif str(userid) == "318418624":
        await session.send("傻狗俩星还在叫")
    # 如果是上号
    elif str(userid) == "1585606107":
        await session.send("摸鱼！逮到！")
    # 如果是弟弟
    elif str(userid) == "630986567":
        await session.send("弟弟这么闲，建议去帮我凹深渊")
    else:
        await session.send("让识宝看看是谁在水群")


@on_natural_language(keywords={}, only_to_me=False)
async def _(session: NLPSession):
    # 有25%的概率触发自动回复
    req_num = random.randint(0, 100)
    log.info("随机数为：" + str(req_num))
    if req_num <= 25:
        return IntentCommand(65, "waterB")
    else:
        pass
