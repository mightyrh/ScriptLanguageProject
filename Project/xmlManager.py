#초단기실황조회

from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
from xmlreal_time_weather import*


xmlFD = -1
xml_Doc = None

#### xml 관련 함수 구현
def LoadXMLFromFile():
    fileName = str(input ("please input file name to load :"))
    global xmlFD, xml_Doc
    try:
        xmlFD = open(fileName, 'r', encoding = 'UTF-8')
    except IOError:
        print ("invalid file name or path")
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            xml_Doc = dom
            return dom
    return None

def BooksFree():
    if checkDocument():
        xml_Doc.unlink()

def PrintDomtoXML():
    if checkDocument():
        print(xml_Doc.toxml())

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # get Dom Implementation
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # create bold element
        b = newdoc.createElement('b')
        # create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)

        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        # create title Element
        p = newdoc.createElement('p')
        # create text node
        titleText = newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  # line end

    # append Body
    top_element.appendChild(body)

    return newdoc.toxml()

def checkDocument():
    global xml_Doc
    if xml_Doc == None:
        print ("Error : Document is empty")
        return False
    return True

def PrintXmlData():
    global xml_Doc
    if not checkDocument():
        return None

    weather = xml_Doc.childNodes
    response = weather[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    for item in items:
        data = item.childNodes
        for element in data:
            if element.nodeName == "baseDate":
                print("Date = ", element.firstChild.nodeValue)
            elif element.nodeName == "baseTime":
                print("Time = ", element.firstChild.nodeValue)
            elif element.nodeName == "nx":
                print("x좌표 = ", element.firstChild.nodeValue)
            elif element.nodeName == "ny":
                print("y좌표 = ", element.firstChild.nodeValue)

def PrintWeatherData(data):
    print("날짜 : ", data['date'])
    print("시간 : ", data['time'])
    print("x좌표 : ", data['x'])
    print("y좌표 : ", data['y'])
    print("기온 : ", data['temp'])
    print("습도 : ", data['humidity'])