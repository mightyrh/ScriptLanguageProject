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

def PrintDomtoXML():
    if checkDocument():
        print(xml_Doc.toxml())



def checkDocument():
    global xml_Doc
    if xml_Doc == None:
        print ("Error : Document is empty")
        return False
    return True

def PrintWeather():
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