import time
import telepot
from datetime import datetime
from telepot.loop import MessageLoop
#import requests
import sys
from weatherForecast import*
from apiService import getApi_air_quality_forecast

bot = telepot.Bot('503466231:AAFjBE66R0YzptpGDb6OPsjuQHaBDh2A-6Y')
citySelected = False
forecastType = ""
#메세지가 올 때마다 loop되고 있는 함수 (메세지 처리 및 발송)
def handle(msg):
    global citySelected, forecastType
    # 메세지의 content_type, chat_type, chat_id 를 저장
    content_type, chat_type, chat_id = telepot.glance(msg)
    # 처리를 확인할 수 있게 화면상에 print
    print(content_type, chat_type, chat_id)

    # message content type 이 text일때만
    if content_type == 'text':
        if msg['text'] == '오늘날씨' and citySelected == False:  # message 내용이 '오늘날씨' 이면
            citySelected = True
            forecastType = "오늘날씨"
            bot.sendMessage(chat_id, '지역 이름을 입력해주세요. (예, 원주시)') # 안녕하세요 를 sendMessage 한다
        elif citySelected == True and forecastType == "오늘날씨":
            city = msg['text']
            GeoData = SearchGeo(city)
            for data in GeoData['mapdata']['results'][0]['address_components']:
                if 'administrative_area_level_1' in data['types']:
                    location = data['long_name']
            PM10_level, air_quality = getApi_air_quality_forecast(location)
            base_date = dateCalculate('0200')
            year = base_date.strftime("%Y")
            month = base_date.strftime("%m")
            day = base_date.strftime("%d")
            bot.sendMessage(chat_id, "날짜: " + year + "년 " + month + "월 " + day + "일" + "\n\n")
            bot.sendMessage(chat_id, "현재 미세먼지 농도 : " + PM10_level + " " + air_quality + "\n\n")
            data = getApi_weather_for_a_day(GeoData['x'], GeoData['y'], "today")
            bot.sendMessage(chat_id, weather_for_today(data))
            citySelected = False
        else:
            #모르는 명령어 입력시
            bot.sendMessage(chat_id, '제대로된 입력을 해주세요.')
            citySelected = False

def botMessageLoop():
    bot.message_loop(handle)    # loop
    while 1:
        time.sleep(10)
