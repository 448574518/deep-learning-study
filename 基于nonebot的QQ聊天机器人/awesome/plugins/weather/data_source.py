import requests
import json


async def weather_report_of_city(city: str) -> str:
    # 拿到城市后，需要先查询城市的locationID
    loc_url = "https://geoapi.qweather.com/v2/city/lookup?"
    loc_params = {
        # key是在和风天气创建的key
        "key": "bc71bb6345f84c8ebd3422f781097cc5",
        "location": str(city),
        # 限定地区范围为中国
        "range": "cn"
    }
    loactionID = ''
    wea_now = ""
    location_response = requests.get(loc_url, loc_params)
    location_response = json.loads(location_response.text)
    if location_response['code'] == "200":
        location_response = location_response['location']
        for area in location_response:
            # 如果是目标城市，则获取id
            if area['name'] == city:
                loactionID = area['id']
    else:
        wea_now = f"查询城市:{city}的信息失败，网络似乎开小差了。。。"
    # 获取城市的天气信息
    """
    接口返回实例
    {
      "code": "200",
      "updateTime": "2020-06-30T22:00+08:00",
      "fxLink": "http://hfx.link/2ax1",
      "now": {
        "obsTime": "2020-06-30T21:40+08:00",    （更新时间）
        "temp": "24",   （温度）
        "feelsLike": "26",  （体感温度）
        "icon": "101",
        "text": "多云",   （天气）
        "wind360": "123",   （360风向）
        "windDir": "东南风",   （风向）
        "windScale": "1",   （风级）
        "windSpeed": "3",   （风速，km/h）
        "humidity": "72",
        "precip": "0.0",
        "pressure": "1003",
        "vis": "16",
        "cloud": "10",
        "dew": "21"
      },
      "refer": {
        "sources": [
          "QWeather",
          "NMC",
          "ECMWF"
        ],
        "license": [
          "commercial license"
        ]
      }
    }
    """
    if loactionID:
        # 如果成功获取到城市id
        weather_url = "https://devapi.qweather.com/v7/weather/now?"
        weather_params = {
            # key是在和风天气创建的key
            "key": "bc71bb6345f84c8ebd3422f781097cc5",
            "location": str(loactionID),
        }
        weather_response = requests.get(weather_url, weather_params)
        weather_response = json.loads(weather_response.text)
        weather_now = weather_response['now']
        wea_now = f"{city}当前的温度为：" + str(weather_now['temp']) + ",体感温度为：" + str(weather_now['feelsLike'])
        wea_now += ",天气：" + str(weather_now['text']) + ",风力等级：" + str(weather_now['windScale']) + ",风速"
        wea_now += str(weather_now['windSpeed']) + "公里/小时"
    else:
        wea_now = f"获取城市:{city}的信息失败，你输入的真的是正确存在的城市嘛？"

    return wea_now