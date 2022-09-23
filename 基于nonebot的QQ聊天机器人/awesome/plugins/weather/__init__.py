from nonebot import on_command, CommandSession
from nonebot import NLPSession, on_natural_language, IntentCommand
from jieba import posseg

from .data_source import weather_report_of_city


# on_command装饰器将函数声明为一个命令处理器
# 这里的weather为命令的名字，同时还可以是'天气'、'天气预报'、'查天气'
@on_command('weather', aliases={'天气', '天气预报', '查天气'}, only_to_me=False)
async def weather(session: CommandSession):
    # 获取当前消息的内容并且去掉空格
    city = session.current_arg_text.strip()
    # 如果除了命令的名字之外，用户还提供了别的内容，即用户直接将城市跟在命令后面，则此时的city不为空。例如用户可能发送了'天气 郑州'，
    # 则此时city == '郑州'，否则的话，表明用户仅发送了'天气'，city为空，机器人就会发送一条消息并且等候
    if not city:
        city = (await session.aget(prompt='请问你想查询那个城市的天气呢？')).strip()
        # 如果用户发的还是空白，那就继续询问
        while not city:
            city = (await session.aget(prompt='查询的城市名称不能为空哦，请再次输入')).strip()
    # 获取天气
    weather_report = await weather_report_of_city(city)
    await session.send(weather_report)


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords="天气", only_to_me=False)
async def _(session: NLPSession):
    # 先去掉空格
    strip_msg = session.msg_text.strip()
    # 分词并且进行词性标注
    words = posseg.lcut(strip_msg)
    # 取出第一个词性为城市的词
    city = None
    for word in words:
        # 每次词都是一个pair对象，包含word和flag两个属性，分别是词和词性
        if word.flag == "ns":
            city = word.word
            break
    # 这里的90叫做置信度，这个如果有多个处理器，会根据置信度来排序处理，只有置信度大于60的才会被执行
    # 换句话说，置信度表示对「当前用户输入的意图是触发某命令」这件事有多大把握，应理解为普通意义的「confidence」。
    # 第二个参数是调用的方法
    return IntentCommand(90, "weather", current_arg=city or '')  # 如果 city 为空，则给 current_arg 传入空字符串

