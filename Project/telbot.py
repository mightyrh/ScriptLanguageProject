import time
import telepot
from datetime import datetime
from telepot.loop import MessageLoop
#import requests
import sys
from weatherForecast import*

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
            bot.sendMessage(chat_id, weather_for_today(city))
            citySelected = False
        else:
            #모르는 명령어 입력시
            bot.sendMessage(chat_id, '제대로된 입력을 해주세요.')
            citySelected = False

def botMessageLoop():
    bot.message_loop(handle)    # loop
    while 1:
        time.sleep(10)
