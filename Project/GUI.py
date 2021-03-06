from tkinter import *

from tkinter import font
import map
import tkinter.messagebox
from PIL import Image, ImageTk
from gmail import*
from telbot import*
from multiprocessing import Process, Queue
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import font_manager,rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/H2PORL.TTF").get_name()
rc('font', family=font_name)

day_clear = Image.open('day_clear.png')
day_cloud_little = Image.open('day_cloud_little.png')
day_cloud_alot = Image.open('day_cloud_alot.png')
day_rain = Image.open('day_rain.png')
day_rain_snow = Image.open('day_rain_snow.png')
day_snow = Image.open('day_snow.png')

night_clear = Image.open('night_clear.png')
night_cloud_little = Image.open('night_cloud_little.png')
night_cloud_alot = Image.open('night_cloud_alot.png')
night_rain = Image.open('night_rain.png')
night_rain_snow = Image.open('night_rain_snow.png')
night_snow = Image.open('night_snow.png')

matplotlib.use('TkAgg')

g_Tk = Tk()
g_Tk.geometry("850x850+750+200")
g_Tk.title("오늘의 날씨는?")

DataList = []
def InitBack():
    global BackGroundImage
    global BackGround

    BackGroundImage = Image.open('BackGround.png')
    BackGroundImage = ImageTk.PhotoImage(BackGroundImage)

    BackGround = Canvas(g_Tk, height=900, width=850)
    BackGround.create_image(425, 300, image=BackGroundImage)
    BackGround.pack()
    BackGround.place(x=0, y=0)

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[오늘의 날씨는?]")
    MainText.pack()
    MainText.place(x=20)

def InitSearchListBox():
    global SearchOption
    OptionScrollbar = Scrollbar(g_Tk)

    SearchOption =Text(g_Tk,height = 1,width = 10,borderwidth = 12, relief = 'ridge')
    SearchOption.insert(INSERT,"오늘날씨\n")
    SearchOption.insert(END, "10일날씨")

    OptionScrollbar.config(command=SearchOption.yview)
    SearchOption.config(yscrollcommand = OptionScrollbar.set)

    OptionScrollbar.pack()
    OptionScrollbar.place(x=130,y=46)
    SearchOption.pack()
    SearchOption.place(x=20,y=50)

    SearchOption.configure(state ='disabled')


def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=10, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=105)




def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375,y=200)

    RenderText = Text(g_Tk,width =49,height = 14,borderwidth=12,relief='ridge',yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10,y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT,fill=BOTH)

    RenderText.configure(state='disabled')



def InitButton():
    button = Button(g_Tk,text="검색",command=ButtonAction)
    button.pack()
    button.place(x=280,y=110)

def InitSendButton():
    button = Button(g_Tk, text="이메일", command=ButtonSend)
    button.pack()
    button.place(x=330, y=110)

def InitMapLabel():
    global mapLabel
    mapLabel = Label(g_Tk,height=26,width=56,borderwidth=12,relief='ridge')
    mapLabel.pack()
    mapLabel.place(x=400,y=0)


def ButtonAction():
    global InputLabel
    global RenderText

    global currentTempHumidity
    global mapdata
    global GeoData

    temps = []
    humidities = []
    icons = []
    Option = str(int(float(SearchOption.yview()[1])*2))
    print(SearchOption.get(Option+".0"))

    address = InputLabel.get()
    GeoData = map.SearchGeo(address)
    mapdata = GeoData['mapdata']
    todayData = getApi_weather_for_a_day(GeoData['x'], GeoData['y'], "today")
    lat = mapdata['results'][0]['geometry']['location']['lat']
    lng = mapdata['results'][0]['geometry']['location']['lng']

    for data in GeoData['mapdata']['results'][0]['address_components']:
        if 'locality' in data['types']:
            cityName = data['long_name']
        elif 'administrative_area_level_1' in data['types']:
            location = data['long_name']

    RenderText.configure(state='normal')
    RenderText.delete(0.0,END)

    im = Image.open(BytesIO(map.mapimage(lat,lng)))
    image = ImageTk.PhotoImage(im)

    global mapLabel
    mapLabel = Label(g_Tk, image=image, height=400, width=400,borderwidth=12,relief='ridge')
    mapLabel.image = image
    mapLabel.pack()
    mapLabel.place(x=400, y=0)

    if Option == '1' and GeoData['x'] != "error":
        currentTempHumidity = getApi_real_time_weather(GeoData['x'], GeoData['y'])
        weatherForToday = weather_for_today(todayData)
        PM10_level, air_quality = getApi_air_quality_forecast(location)
        RenderText.insert(INSERT,"날짜")
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, currentTempHumidity['date'])
        RenderText.insert(INSERT, "\t")
        RenderText.insert(INSERT, currentTempHumidity['time'])
        RenderText.insert(INSERT, "]")
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, mapdata["results"][0]["formatted_address"])
        RenderText.insert(INSERT, "\n현재온도 :")
        RenderText.insert(INSERT, currentTempHumidity['temp'] + "도")
        RenderText.insert(INSERT, "\n현재습도 :")
        RenderText.insert(INSERT, currentTempHumidity['humidity'] + "%")
        RenderText.insert(INSERT, "\n현재 미세먼지농도 : ")
        RenderText.insert(INSERT, PM10_level)
        RenderText.insert(INSERT, ", ")
        RenderText.insert(INSERT, air_quality)
        RenderText.insert(INSERT, "\n\n")
        RenderText.insert(INSERT, weatherForToday)

        for time in todayData:
            temps.append(todayData[time]['T3H'])
            humidities.append(todayData[time]['REH'])

        drawGraph(temps, humidities, 'today')
        icons = getIcons(todayData, 'today')
        drawIcons(icons)


    elif Option == '2' and GeoData['x'] != 'error':
        minTemps = []
        maxTemps = []
        minmaxTemp = ['taMin3', 'taMax3', 'taMin4', 'taMax4', 'taMin5', 'taMax5', 'taMin6', 'taMax6', 'taMin7', 'taMax7', 'taMin8', 'taMax8', 'taMin9', 'taMax9', 'taMin10', 'taMax10']
        forecasts = getApi_medium_term_forecast(cityName)  # 3~10일짜리
        temperatures = getApi_medium_term_temperature(cityName)
        todayData = getApi_weather_for_a_day(GeoData['x'], GeoData['y'], 'today')
        tomorrowData = getApi_weather_for_a_day(GeoData['x'], GeoData['y'], 'tomorrow')

        mediumTermSkies = {'today': todayData, 'tomorrow': tomorrowData, 'medium': forecasts}

        minTemps.append(str(int(float(todayData['0600']['TMN']))))
        minTemps.append(str(int(float(tomorrowData['0600']['TMN']))))
        maxTemps.append(str(int(float(todayData['1500']['TMX']))))
        maxTemps.append(str(int(float(tomorrowData['1500']['TMX']))))

        for i in range(0, 16):
            if i % 2 == 0:
                minTemps.append(temperatures[minmaxTemp[i]])
            elif i % 2 == 1:
                maxTemps.append(temperatures[minmaxTemp[i]])
        drawGraph(maxTemps, minTemps, 'medium')

        medium_term_weather_text(todayData, tomorrowData, forecasts, temperatures)
        icons = getIcons(mediumTermSkies, 'medium')
        drawIcons(icons)

    else:
        RenderText.insert(INSERT,"제대로된 주소를 입력해주세요")

    RenderText.configure(state='disabled')

def drawIcons(icons):
    global imgs
    imgs = []
    if len(icons) == 8:
        for i in range(0,8):
            icon = Image.open(icons[i])
            imgs.append(ImageTk.PhotoImage(icon))
            BackGround.create_image(150 + i * 80, 520, image=imgs[i])
            BackGround.pack()
            BackGround.place(x=0, y=0)
    elif len(icons) == 10:
        for i in range(0,10):
            icon = Image.open(icons[i])
            imgs.append(ImageTk.PhotoImage(icon))
            BackGround.create_image(135 + i * 65, 520, image=imgs[i])
            BackGround.pack()
            BackGround.place(x=0, y=0)

# dict로 하늘 정보 가져옴 실시간 날씨는 그냥 데이터 통째로 가져옴
def getIcons(skyDict, forecastType):
    timeList = ['0600', '0900', '1200', '1500', '1800', '2100', '0000', '0300']
    mediumSkyList = ['wf3Pm', 'wf4Pm', 'wf5Pm', 'wf6Pm', 'wf7Pm', 'wf8', 'wf9', 'wf10']
    skyList = []
    iconList = []
    dayNight = ''
    if forecastType == 'today':
        for time in timeList:
            if time == '1800' or time == '2100' or time == '0000' or time == '0300':
                dayNight = 'night'
            else:
                dayNight = 'day'
            if skyDict[time]['PTY'] != '0':
                skyList.append([{'PTY' : skyDict[time]['PTY']}, dayNight])
            else:
                skyList.append([{'SKY' : skyDict[time]['SKY']}, dayNight])
        #여기서 리스트에 있는 코드들을 파일 이름으로 바꿔서 다른 리스트에 담고 리턴해준다.
        for sky in skyList:
            if sky[0] == {'SKY' : '1'}:
                if sky[1] == 'day':
                    iconList.append('day_clear.png')
                else:
                    iconList.append('night_clear.png')
            elif sky[0] == {'SKY' : '2'}:
                if sky[1] == 'day':
                    iconList.append('day_cloud_little.png')
                else:
                    iconList.append('night_cloud_little.png')
            elif sky[0] == {'SKY' : '3'} or sky[0] == {'SKY' : '4'}:
                if sky[1] == 'day':
                    iconList.append('day_cloud_alot.png')
                else:
                    iconList.append('night_cloud_alot.png')
            elif sky[0] == {'PTY' : '1'}:
                if sky[1] == 'day':
                    iconList.append('day_rain.png')
                else:
                    iconList.append('night_rain.png')
            elif sky[0] == {'PTY' : '2'}:
                if sky[1] == 'day':
                    iconList.append('day_rain_snow.png')
                else:
                    iconList.append('night_rain_snow.png')
            elif sky[0] == {'PTY' : '3'}:
                if sky[1] == 'day':
                    iconList.append('day_snow.png')
                else:
                    iconList.append('night_snow.png')
        return iconList
    elif forecastType == 'medium':
        if skyDict['today']['1200']['PTY'] != '0':
            skyList.append({'PTY': skyDict['today']['1200']['PTY']})
        else:
            skyList.append({'SKY': skyDict['today']['1200']['SKY']})

        if skyDict['tomorrow']['1200']['PTY'] != '0':
            skyList.append({'PTY': skyDict['tomorrow']['1200']['PTY']})
        else:
            skyList.append({'SKY': skyDict['tomorrow']['1200']['SKY']})

        for mediumSky in mediumSkyList:
            sky = skyDict['medium'][mediumSky]
            if sky == '맑음':
                skyList.append('day_clear.png')
            elif sky == '구름조금':
                skyList.append('day_cloud_little.png')
            elif sky == '구름많음' or sky == '흐림':
                skyList.append('day_cloud_alot.png')
            elif sky == '구름많고 비' or sky == '흐리고 비':
                skyList.append('day_rain.png')
            elif sky == '구름많고 눈' or sky == '흐리고 눈':
                skyList.append('day_snow.png')
            elif sky == '구름많고 비/눈' or sky == '흐리고 비/눈':
                skyList.append('day_rain_snow.png')
            elif sky == '구름많고 눈/비' or sky == '흐리고 눈/비':
                skyList.append('day_rain_snow.png')

        for sky in skyList:
            if sky == {'SKY': '1'}:
                iconList.append('day_clear.png')
            elif sky == {'SKY': '2'}:
                iconList.append('day_cloud_little.png')
            elif sky == {'SKY': '3'}:
                iconList.append('day_cloud_alot.png')
            elif sky == {'PTY': '1'}:
                iconList.append('day_rain.png')
            elif sky == {'PTY': '2'}:
                iconList.append('day_rain_snow.png')
            elif sky == {'PTY': '3'}:
                iconList.append('day_snow.png')
            else:
                iconList.append(sky)

        return iconList

def medium_term_weather_text(todayData, tomorrowData, forecasts, temperatures):
    global GeoData
    cityName = ''

    time = dateCalculate('0000')

    printNearWeatherText(time,todayData)
    tomorrowTime = time + datetime.timedelta(1)
    printNearWeatherText(tomorrowTime, tomorrowData)

    for data in GeoData['mapdata']['results'][0]['address_components']:
        if 'locality' in data['types']:
            cityName = data['long_name']
    mediumTermWeather3to10Text(time, forecasts, temperatures)


def printNearWeatherText(timeData, weatherData):
    timeList = ['0600', '0900', '1200', '1500', '1800', '2100', '0000']
    sky = 0
    rainType = 0

    for time in timeList:
        if int(weatherData[time]['SKY']) > sky:
            sky = int(weatherData[time]['SKY'])

    for time in timeList:
        if int(weatherData[time]['PTY']) > rainType:
            rainType = int(weatherData[time]['PTY'])

    if sky == 1:
        skyText = '맑음'
    elif sky == 2:
        skyText = '구름조금'
    elif sky == 3:
        skyText = '구름많음'
    elif sky == 4:
        skyText = '흐림'

    if rainType == 0:
        rainTypeText = '없음'
    elif rainType == 1:
        rainTypeText = '비'
    elif rainType == 2:
        rainTypeText = '진눈깨비'
    elif rainType == 3:
        rainTypeText = '눈'

    if rainType != 0:
        forecast = rainTypeText
    else:
        forecast = skyText

    RenderText.insert(INSERT, "[")
    RenderText.insert(INSERT, timeData.strftime('%Y') + '년 ' + timeData.strftime('%m') + '월 ' + timeData.strftime('%d') + '일]')
    RenderText.insert(INSERT, "\n")
    RenderText.insert(INSERT, forecast + '\n')
    RenderText.insert(INSERT, '최저온도' + str(weatherData['0600']['TMN']) + '\n')
    RenderText.insert(INSERT, '최고온도' + str(weatherData['1500']['TMX']) + '\n')
    RenderText.insert(INSERT, "\n")
    RenderText.insert(INSERT, "\n")

def mediumTermWeather3to10Text(timeData, forecasts, temperatures):
    #forecasts = getApi_medium_term_forecast(cityName)
    #temperatures = getApi_medium_term_temperature(cityName)

    for i in range(3,10):
        if i == 3:
            forecastDate = 'wf3Pm'
            minTemp = 'taMin3'
            maxTemp = 'taMax3'
        elif i == 4:
            forecastDate = 'wf4Pm'
            minTemp = 'taMin4'
            maxTemp = 'taMax4'
        elif i == 5:
            forecastDate = 'wf5Pm'
            minTemp = 'taMin5'
            maxTemp = 'taMax5'
        elif i == 6:
            forecastDate = 'wf6Pm'
            minTemp = 'taMin6'
            maxTemp = 'taMax6'
        elif i == 7:
            forecastDate = 'wf7Pm'
            minTemp = 'taMin7'
            maxTemp = 'taMax7'
        elif i == 8:
            forecastDate = 'wf8'
            minTemp = 'taMin8'
            maxTemp = 'taMax8'
        elif i == 9:
            forecastDate = 'wf9'
            minTemp = 'taMin9'
            maxTemp = 'taMax9'
        elif i == 10:
            forecastDate = 'wf10'
            minTemp = 'taMin10'
            maxTemp = 'taMax10'

        time = timeData + datetime.timedelta(i)
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, time.strftime('%Y') + '년 ' + time.strftime('%m') + '월 ' + time.strftime('%d') + '일]')
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, forecasts[forecastDate] + '\n')
        RenderText.insert(INSERT, '최저온도' + str(temperatures[minTemp]) + '\n')
        RenderText.insert(INSERT, '최고온도' + str(temperatures[maxTemp]) + '\n')
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "\n")

def ButtonSend():

    emailText = RenderText.get(1.0, END)
    sendEmail(emailText)

def InitGraph():
    global canvas
    global toolbar
    f=matplotlib.figure.Figure(figsize=(5,3),dpi=100)
    a = f.add_subplot(111)
    x_value = [0, 0, 0, 0]
    y_value = [0, 0, 0, 0]
    x2_value = [0, 0, 0, 0]
    y2_value = [0, 0, 0, 0]

    axis = a.plot()
    bar = a.bar(x_value, y_value, linewidth=0.1, label='tem', color='r')
    a.set_xlabel('Time',color='g')
    a.set_ylabel('Tem',color='r')

    a2 = a.twinx()
    bar2 = a2.bar(x2_value, y2_value, linewidth=0.1, label='hum', color='b')
    a2.set_ylabel('Hum', color='b')
    f.legend()

    canvas = FigureCanvasTkAgg(f, g_Tk)
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)

    #label = Label(root, image=image, height=400, width=400)
    #label.pack()
    #label.place(x=0, y=0)


def drawGraph(graph1Data, graph2Data, graphType):
    global canvas
    plt.rcParams['axes.unicode_minus'] = False
    canvas.get_tk_widget().pack_forget()
    timeList = ['0600', '0900', '1200', '1500', '1800', '2100', '0000', '0300']
    dayList = []
    date = dateCalculate('0600')
    for i in range(0, 10):
        if i == 2:
            date += datetime.timedelta(1)
        dayList.append(date.strftime('%m') + ' ' + date.strftime('%d'))
        date += datetime.timedelta(1)

    f = matplotlib.figure.Figure(figsize=(5, 3), dpi=100)
    a = f.add_subplot(111)

    x_value = []
    y_value = []
    y2_value = []

    if len(graph1Data) == 8:
        for i in range(0, len(graph1Data)):
            x_value.append(timeList[i])
    elif len(graph1Data) == 10:
        for i in range(0, len(graph1Data)):
            x_value.append(dayList[i])

    for data in graph1Data:
        y_value.append(int(data))

    #for i in range(1, len(humidities)+1):
    #    x2_value.append(i*2)

    for data in graph2Data:
        y2_value.append(int(data))

    axis = a.plot(x_value, y_value, color='r')
    a.grid(True)
    a.set_xlabel('시간', color='g')

    if graphType == 'today':
        a.set_ylabel('기온', color='r')
        a.set_ylim([-10, 40])
        a2 = a.twinx()
        bar2 = a2.bar(x_value, y2_value, width=0.3, label='hum', color='b')
        a2.set_ylabel('습도', color='b')
        a2.set_ylim(0,300)
        #f.legend()

    elif graphType == 'medium':
        a.set_ylabel('최고기온', color='r')
        a.set_ylim([-10, 40])
        a2 = a.twinx()
        a2.plot(x_value, y2_value, color='b')
        a2.set_xlabel('날짜', color='g')
        a2.set_ylabel('최저기온', color='b')
        a2.set_ylim([-10, 40])


    canvas = FigureCanvasTkAgg(f, g_Tk)
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)

    # label = Label(root, image=image, height=400, width=400)
    # label.pack()
    # label.place(x=0, y=0)


if __name__ == '__main__':

    InitBack()
    InitTopText()
    InitMapLabel()
    InitSearchListBox()
    InitInputLabel()
    InitButton()
    InitSendButton()
    InitRenderText()
    InitGraph()


    procs = []
    proc = Process(target=botMessageLoop, args=())
    procs.append(proc)
    proc.start()

    g_Tk.mainloop()

    for proc in procs:
        proc.join()