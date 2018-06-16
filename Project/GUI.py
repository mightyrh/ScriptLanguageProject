from tkinter import *

from tkinter import font
import map
import tkinter.messagebox
from PIL import Image, ImageTk
from gmail import*
from telbot import*
from multiprocessing import Process, Queue
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

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
g_Tk.geometry("850x900+750+200")
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
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',width=10, height=1, borderwidth=12, relief='ridge',yscrollcommand=ListBoxScrollbar.set)

    SearchListBox.insert(1, "오늘날씨")
    SearchListBox.insert(2, "10일간 날씨")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)

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

    address = InputLabel.get()
    GeoData = map.SearchGeo(address)
    mapdata = GeoData['mapdata']
    lat = mapdata['results'][0]['geometry']['location']['lat']
    lng = mapdata['results'][0]['geometry']['location']['lng']

    RenderText.configure(state='normal')
    RenderText.delete(0.0,END)

    im = Image.open(BytesIO(map.mapimage(lat,lng)))
    image = ImageTk.PhotoImage(im)

    global mapLabel
    mapLabel = Label(g_Tk, image=image, height=400, width=400,borderwidth=12,relief='ridge')
    mapLabel.image = image
    mapLabel.pack()
    mapLabel.place(x=400, y=0)

    showWeatherIcon()

    if GeoData['x'] != "error":
        currentTempHumidity = getApi_real_time_weather(GeoData['x'], GeoData['y'])
        weatherForToday = weather_for_today(GeoData['x'], GeoData['y'])
        PM10_level, air_quality = getApi_air_quality_forecast(mapdata['results'][0]['address_components'][1]['long_name'])
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

        drawGraph()


    else:
        RenderText.insert(INSERT,"제대로된 주소를 입력해주세요")

    RenderText.configure(state='disabled')


def ButtonSend():

    emailText = "날짜" + "[" + currentTempHumidity['date'] + "\t" + currentTempHumidity['time'] + "]" + "\n" + \
                mapdata["results"][0]["formatted_address"] + "\n" + \
                "온도 :" + currentTempHumidity['temp'] + ", 습도 :" + currentTempHumidity['humidity']
    sendEmail(emailText)

def showWeatherIcon():

    BackGround.configure(state='normal')
    day_clear = Image.open('day_clear.png')
    day_clear = ImageTk.PhotoImage(day_clear)
    BackGround.create_image(190, 460, image=day_clear)
    BackGround.pack()
    BackGround.place(x=100, y=200)
    BackGround.configure(state='disable')

def InitGraph():
    global canvas

    f=matplotlib.figure.Figure(figsize=(5,4),dpi=100)
    a = f.add_subplot(111)
    x_value = [1, 3, 5, 7]
    y_value = [3, 9, 15, 21]
    x2_value = [2, 4, 6, 8]
    y2_value = [3, 9, 15, 21]

    axis = a.plot()
    bar = a.bar(x_value, y_value, linewidth=0.5, label='tem', color='r')
    a.set_xlabel('Time',color='g')
    a.set_ylabel('Tem',color='r')

    a2 = a.twinx()
    bar2 = a2.bar(x2_value, y2_value, linewidth=0.5, label='hum', color='b')
    a2.set_ylabel('Hum', color='b')
    f.legend()

    canvas = FigureCanvasTkAgg(f, g_Tk)
    toolbar = NavigationToolbar2TkAgg(canvas, g_Tk)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)

    #label = Label(root, image=image, height=400, width=400)
    #label.pack()
    #label.place(x=0, y=0)


def drawGraph():
    global canvas
    canvas.get_tk_widget().pack_forget()

    f = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(111)
    x_value = [1, 3, 5, 7]
    y_value = [3, 9, 15, 21]
    x2_value = [2, 4, 6, 8]
    y2_value = [100, 1000, 100000, 80000]

    axis = a.plot()
    bar = a.bar(x_value, y_value, linewidth=0.5, label='tem', color='r')
    a.set_xlabel('Time', color='g')
    a.set_ylabel('Tem', color='r')

    a2 = a.twinx()
    bar2 = a2.bar(x2_value, y2_value, linewidth=0.5, label='hum', color='b')
    a2.set_ylabel('Hum', color='b')
    f.legend()


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