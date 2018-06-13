import time
import telepot
from datetime import datetime
from telepot.loop import MessageLoop
#import requests
import sys

bot = telepot.Bot('503466231:AAFjBE66R0YzptpGDb6OPsjuQHaBDh2A-6Y')

#메세지가 올 때마다 loop되고 있는 함수 (메세지 처리 및 발송)
def handle(msg):
    # 메세지의 content_type, chat_type, chat_id 를 저장
    content_type, chat_type, chat_id = telepot.glance(msg)
    # 처리를 확인할 수 있게 화면상에 print
    print(content_type, chat_type, chat_id)

    # message content type 이 text일때만
    if content_type == 'text':
        if msg['text'] == '안녕':  # message 내용이 '안녕' 이면
            bot.sendMessage(chat_id, '안녕하세요 !') # 안녕하세요 를 sendMessage 한다
        elif msg['text'] == '뭐해':
            bot.sendMessage(chat_id, '아무것도')
        else:
            #모르는 명령어 입력시
            bot.sendMessage(chat_id, '제대로된 입력을 해주세요.')

def botMessageLoop():
    bot.message_loop(handle)    # loop
    while 1:
        time.sleep(10)
