loopFlag = 1
from apiManager import *


#### Menu  implementation
def printMenu():
    print("₩nWelcome! Weather Forecast Program (api version)")
    print("========Menu==========")
    print("Get Current Weather: c")
    print("Get Weather Forecast: f")
    print("send maIl : i")
    print("Quit program:   q")
    print("========Menu==========")

def launcherFunction(menu):
    if menu == "c":
        getData_real_time_weather()
#    elif menu == "f":
#        get_weather_forecast()
    elif menu == 'q':
       QuitBookMgr()

    elif menu == "t":
        date = str(input("날자를 입력하세요 ex) 20180528 : "))
        time = str(input("시간을 입력하세요 ex) 0600 : "))
        x = str(input("x좌표를 입력하세요 ex) 60 : "))
        y = str(input("y좌표를 입력하세요 ex) 127 : "))
        data = getApi_real_time_weather(date, time, x, y)
        PrintWeatherData(data)


    else:
        print ("error : unknow menu key")

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()

while (loopFlag > 0):
    printMenu()
    menuKey = str(input('select menu :'))
    launcherFunction(menuKey)