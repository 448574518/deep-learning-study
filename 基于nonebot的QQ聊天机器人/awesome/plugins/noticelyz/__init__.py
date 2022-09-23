import asyncio
import random

import nonebot
import logging
import time
from aiocqhttp.exceptions import Error as CQhttpErr
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from nonebot import CommandSession, scheduler, on_command

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = logging.getLogger(__name__)
# trigger = AndTrigger([IntervalTrigger(minutes=30), CronTrigger(day_of_week='0-4', hour=17)])
# trigger = AndTrigger([IntervalTrigger(seconds=10), CronTrigger(day_of_week='0-4', hour=17)])


notice_dic = {
    "1": "你最好已经打卡了，识宝可不想再来提醒你",
    "2": "打卡了吗？你就上DNF",
    "3": "打卡打卡，不会还没下班吧，真可怜",
    "4": "我是识宝，是来提醒你打卡的，快说：谢谢识宝",
    "5": "就TM你天天不打卡是吧",
    "6": "我是识宝，抓紧V50，不然后面是否提醒你打卡，就要看我心情了",
    "7": "还不下班打卡？你以为识宝很闲嘛？"
}
end_reply = {
    "1": "哦",
    "2": "识宝知道了，你可以退下了",
    "3": "你终于记得打卡了，建议给李徐繁买套国庆",
    "4": "what's up,好快",
    "5": "别多BB，抓紧上号"
}
stop_time_word = True
notice_lyz = False


# @nonebot.scheduler.scheduled_job('cron', day_of_week='0-4', hours=17, minutes=30)
@nonebot.scheduler.scheduled_job('cron', day_of_week='0-4', hour=17, minute=30)
async def _():
    bot = nonebot.get_bot()
    cq = r'[CQ:at,qq=1585606107]'
    global notice_lyz
    global stop_time_word
    notice_lyz = True
    while stop_time_word:
        notice_num = random.randint(1, 7)
        notice = notice_dic[str(notice_num)]
        # 随机询问lyz
        await bot.send_group_msg(group_id=1105237910, message=cq + notice)
        # 睡30分钟
        await asyncio.sleep(3000)
        # time.sleep(10)
    notice_lyz = False
    logging.info("更新nl"+str(notice_lyz))
    stop_time_word = True
    logging.info("成功更新stw" + str(stop_time_word))


# 提醒lyz打卡
@on_command("打卡了", aliases={"谢谢识宝"}, only_to_me=False)
async def notice_lyz(session: CommandSession):
    end_num = random.randint(1, 5)
    end_rep = end_reply[str(end_num)]
    userid = session.event.user_id
    global stop_time_word
    # 防止意外触发
    if notice_lyz and (str(userid) == "1585606107"):
        await session.send(end_rep)
        stop_time_word = False
        logging.info("成功更新stw" + str(stop_time_word))
