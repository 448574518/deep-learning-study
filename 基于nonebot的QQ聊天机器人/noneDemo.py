import nonebot

if __name__ == '__main__':
    # 使用默认配置初始化nonebot包
    nonebot.init()
    # 加载内置模块
    nonebot.load_builtin_plugins()
    # 启动
    nonebot.run(host='127.0.0.1', port=8080)

