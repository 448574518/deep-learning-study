from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# 英雄映射
heroset = {
    "艾希": "22",
    "女警": "51"
}
url_head = "/Users/lixufan/PycharmProjects/deep-learning-study/基于nonebot的QQ聊天机器人"


# 查询英雄信息并且返回
async def getHero(heroname: str):
    heroid = heroset[heroname]
    url = f"https://101.qq.com/#/hero-detail?heroid={heroid}&datatype=fight"
    chrome_option = Options()
    # 设置无边框
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--disable-gpu")
    # 加载Chrome驱动
    service = Service(f"{url_head}/screenShot/chromedriver")
    # 加载配置
    brower = webdriver.Chrome(service=service, options=chrome_option)
    # 设置窗口大小（参数会被x2，1280*800实际位2560*1600）
    brower.set_window_size(1280, 800)
    # 访问目标网址
    brower.get(url)
    img_url = f"{url_head}/screenShot/photos/{heroname}.png"
    brower.save_screenshot(img_url)
    brower.quit()