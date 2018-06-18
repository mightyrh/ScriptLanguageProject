# mightyrh@gmail.com 에서 email 발신합니다.

import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import apiService

def sendEmail(text):
    host = "smtp.gmail.com"  # Gmail SMTP 서버 주소
    port = "587"

    #htmlFileName = "logo.html"

    senderAddr = "ajr7875@gmail.com"
    recipientAddr = "ajr7875@gmail.com" # 내가 나한테

    msg = MIMEText(text)
    msg['Subject'] = "Weather forecast"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr


    # 이미지

    #htmlFD = open(htmlFileName, 'rb')
    #HtmlPart = MIMEText(htmlFD.read(), 'html', _charset = 'UTF-8')
    #htmlFD.close()

    #msg.attach(HtmlPart)

    s = smtplib.SMTP("smtp.gmail.com", 587) # SMTP 서버 설정
    #s.set_debuglevel(1) # 디버깅이 필요할 경우 주석을 푼다.
    #s.ehlo()

    s.starttls()
    s.ehlo()
    s.login("mightyrh@gmail.com","i'msofast")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close
