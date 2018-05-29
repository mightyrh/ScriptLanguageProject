loopFlag = 1
from xmlManager import *
from internetService import *
from map import *

#### Menu  implementation
def printMenu():
    print("₩nWelcome! Book Manager Program (xml version)")
    print("========Menu==========")
    print("Load xml:  l")
    print("Print dom to xml: p")
    print("Quit program:   q")
    print("print Book list: b")
    print("Add new book: a")
    print("sEarch Book Title: e")
    print("Make html: m")
    print("----------------------------------------")
    print("Get book data from isbn: g")
    print("send maIl : i")
    print("sTart Web Service: t")
    print("========Menu==========")

def launcherFunction(menu):
    if menu ==  'l':
        LoadXMLFromFile()

    elif menu == 'q':
       QuitBookMgr()
    elif menu == 'p':
        PrintDomtoXML()
    elif menu == 'b':
        PrintXmlData()
#    elif menu == 'a':
#        ISBN = str(input ('insert ISBN :'))
#        title = str(input ('insert Title :'))
#        AddBook({'ISBN':ISBN, 'title':title})
#    elif menu == 'e':
#        keyword = str(input ('input keyword to search :'))
#        printBookList(SearchBookTitle(keyword))
#    elif menu == 'g':
#        isbn = str(input ('input isbn to get :'))
#        #isbn = '0596513984'
#        ret = getBookDataFromISBN(isbn)
#        AddBook(ret)
#    elif menu == 'm':
#        keyword = str(input ('input keyword code to the html  :'))
#        html = MakeHtmlDoc(SearchBookTitle(keyword))
#        print("-----------------------")
#        print(html)
#        print("-----------------------")
    ##elif menu == 'i':
    ##    sendMain()
    elif menu == "t":
        date = str(input("날자를 입력하세요 ex) 20180528 : "))
        time = str(input("시간을 입력하세요 ex) 0600 : "))
        x = str(input("x좌표를 입력하세요 ex) 60 : "))
        y = str(input("y좌표를 입력하세요 ex) 127 : "))
        data = getApi_real_time(date, time, x, y)
        PrintWeatherData(data)
    elif menu == "m":
        date = str(input("날자를 입력하세요 ex) 20180528 : "))
        time = str(input("시간을 입력하세요 ex) 0600 : "))
        x, y = SerchGeo()

        data = getApi_real_time(date, time, x, y)
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