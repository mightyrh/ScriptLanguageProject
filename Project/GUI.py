from tkinter import *

from tkinter import font
import map
import apiService
import tkinter.messagebox
from io import BytesIO
import urllib.request
from PIL import Image, ImageTk
from gmail import*
from telbot import*
from multiprocessing import Process, Queue
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

g_Tk = Tk()
g_Tk.geometry("850x850+750+200")
DataList = []
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

    SearchListBox.insert(1, "서울")
    SearchListBox.insert(2, "부산")
    SearchListBox.insert(3, "대구")
    SearchListBox.insert(4, "인천")
    SearchListBox.insert(5, "광주")
    SearchListBox.insert(6, "대전")
    SearchListBox.insert(7, "울산")
    SearchListBox.insert(8, "경기")
    SearchListBox.insert(9, "강원")
    SearchListBox.insert(10, "충북")
    SearchListBox.insert(11, "충남")
    SearchListBox.insert(12, "전북")
    SearchListBox.insert(13, "전남")
    SearchListBox.insert(14, "경북")
    SearchListBox.insert(15, "경남")
    SearchListBox.insert(16, "제주")
    SearchListBox.insert(17, "세종")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
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
    button.place(x=330,y=110)

def InitMapLabel():
    global mapLabel
    mapLabel = Label(g_Tk,height=26,width=56,borderwidth=12,relief='ridge')
    mapLabel.pack()
    mapLabel.place(x=400,y=0)

def ButtonAction():
    global InputLabel
    global RenderText
    address = InputLabel.get()
    data = map.SearchGeo(address)
    mapdata = data['mapdata']
    #x, y, cityName, mapdata, mapimage = map.SearchGeo(address)


    RenderText.configure(state='normal')
    RenderText.delete(0.0,END)

    im = Image.open(BytesIO(data['mapimage']))
    image = ImageTk.PhotoImage(im)

    global mapLabel
    mapLabel = Label(g_Tk, image=image, height=400, width=400,borderwidth=12,relief='ridge')
    mapLabel.image = image
    mapLabel.pack()
    mapLabel.place(x=400, y=0)

    if data['x'] != "error":
        data = apiService.getApi_real_time_weather(data['cityName'])
        RenderText.insert(INSERT,"날짜")
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, data['date'])
        RenderText.insert(INSERT, "\t")
        RenderText.insert(INSERT, data['time'])
        RenderText.insert(INSERT, "]")
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, mapdata["results"][0]["formatted_address"])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "온도 :")
        RenderText.insert(INSERT, data['temp'])
        RenderText.insert(INSERT, ", 습도 :")
        RenderText.insert(INSERT, data['humidity'])

        drawGraph()

        emailText = "날짜" + "[" + data['date'] + "\t" + data['time'] + "]" + "\n" + \
                    mapdata["results"][0]["formatted_address"] + "\n" + \
                    "온도 :" + data['temp'] + ", 습도 :" + data['humidity']
        #sendEmail(emailText)

    else:
        RenderText.insert(INSERT,"제대로된 주소를 입력해주세요")

    RenderText.configure(state='disabled')

    RenderText.configure(state='disabled')


def drawGraph():
    f=matplotlib.figure.Figure(figsize=(5,4),dpi=100)
    a = f.add_subplot(111)
    x_value = [1, 3, 5, 7]
    y_value = [3, 9, 15, 21]
    x2_value = [2, 4, 6, 8]
    y2_value = [3, 9, 15, 21]

    bar = a.bar(x_value,y_value,linewidth=0.5,label='tem',color='r')
    bar2 = a.bar(x2_value,y2_value,linewidth=0.5,label='hum',color='b')
    f.legend()

    canvas = FigureCanvasTkAgg(f, g_Tk)
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)


if __name__ == '__main__':

    InitTopText()
    InitMapLabel()
    InitSearchListBox()
    InitInputLabel()
    InitButton()
    InitRenderText()

    procs = []
    proc = Process(target=botMessageLoop, args=())
    procs.append(proc)
    proc.start()

    g_Tk.mainloop()

    for proc in procs:
        proc.join()