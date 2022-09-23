import random

import nonebot
import config
import logging
from os import path
from timework.noticelyz import notice_lyz


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = logging.getLogger(__name__)


if __name__ == '__main__':
    # 使用默认配置初始化nonebot包
    nonebot.init(config)
    # 加载内置模块
    nonebot.load_builtin_plugins()
    # 加载编写好的模块
    nonebot.load_plugins(path.join(path.dirname(__file__), 'awesome', 'plugins'), 'awesome.plugins')
    logging.info("in main!")
    # 启动(config中添加HOST和POST后，这里就不用在写了)
    nonebot.run()
