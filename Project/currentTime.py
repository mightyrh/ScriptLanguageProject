#1시간 단위의 현재 시간을 구함

import datetime

def nowDateTime():
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    nowTime = now.strftime('%H00')

    # 40분 전이라면 1시간 전 날씨를 가져옴
    # 발표가 40분에 나는 것 같음
    if int(now.strftime('%M')) < 40:
        nowTime = str(int(nowTime) - 100)
        if int(nowTime) < 1000:
            nowTime = '0' + nowTime

    return nowDate, nowTime

nowDateTime()