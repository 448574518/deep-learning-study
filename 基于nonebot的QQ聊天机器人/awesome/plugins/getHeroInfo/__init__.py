import nonebot
from nonebot import on_command, CommandSession
from .data_source import getHero
import cv2


# 英雄映射
heroset = {
    "艾希": "22",
    "女警": "51"
}
url_head = "/Users/lixufan/PycharmProjects/deep-learning-study/基于nonebot的QQ聊天机器人"


@on_command('searchHero', aliases={"极地", "大乱斗", "查出装"})
async def searchHero(session: CommandSession):
    # 获取想要查询的英雄名
    heroname = session.current_arg_text.strip()
    # 获取user_i，看看是不是俩星发的
    userid = session.event.user_id
    # 获取群号，后面发送图片用
    groupid = session.event.group_id
    if str(userid) == "318418624":
        await session.send("傻狗俩星别叫了")
    # 同天气，如果对方没有输入英雄，则询问英雄名称
    if not heroname:
        heroname = (await session.aget(prompt='请问你想查询哪一个英雄呢？')).strip()
        # 如果空白，继续询问
        while not heroname:
            heroname = (await session.aget(prompt='没有英雄名字没法查询哦')).strip()
    await getHero(heroname)
    CQ_msg = f'[CQ:image,file=file://{url_head}/screenShot/photos/{heroname}.png,subType=0]'
    msg_url = f"file://{url_head}/screenShot/photos/{heroname}.png"
    # r'[CQ:image,' r'file=' + str(setu_url) + r']'
    CQ_msg = r'[CQ:image,' r'file=' + str(msg_url) + r']'
    bot = nonebot.get_bot()
    result = await bot.send_group_msg(group_id=groupid, message=r'[CQ:image,' r'file=' + str(msg_url) + r']')
    print(result)
    # await session.send()




