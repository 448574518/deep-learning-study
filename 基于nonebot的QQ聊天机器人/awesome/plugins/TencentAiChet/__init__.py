import json
import random

from aiocqhttp.message import escape
from nonebot import CommandSession, on_command
from nonebot import NLPSession, on_natural_language, IntentCommand
from typing import Optional

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models


@on_command('Ai_Chet', only_to_me=False)
async def Ai_Chet(session: CommandSession):
    # 获取可选参数，如果没有获取None
    message = session.state.get('message')

    # 获取腾讯的智能回复
    reply = await get_tencent_reply(session, message)
    if reply:
        # 如果获取了回复，则转义后回复给客户，转义会把消息中的某些特殊字符做转换，避免将它们理解为 CQ 码
        await session.send(escape(reply))
    else:
        await session.send("你说的是个🔨，识宝听不懂！")


async def get_tencent_reply(session: CommandSession, text: Optional[str]) -> Optional[str]:
    # 调用智能机器人API获取回复
    if not text:
        return None
    try:
        cerd = credential.Credential(session.bot.config.TENCENT_BOT_SECRET_ID, session.bot.config.TENCENT_BOT_SECRET_KEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cerd, "ap-guangzhou", clientProfile)

        params = {
            "Query": text
        }
        req = models.ChatBotRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ChatBot(req).to_json_string()
        resp_payload = json.loads(resp)
        return resp_payload.get('Reply')
    except TencentCloudSDKException as err:
        print(err)
        return None


@on_natural_language(keywords={}, only_to_me=False)
async def _(session: NLPSession):
    # 如果没有明确的被捕获到的关键词，则尝试调用智能对话
    # 50%的概率
    req_num = random.randint(0, 100)
    # 设置大于100，不会触发腾讯回复
    if req_num > 100:
        # 置信度设置为60，保证是在所有的其他命令之后触发
        return IntentCommand(60, "Ai_Chet", args={"message": session.msg_text})
