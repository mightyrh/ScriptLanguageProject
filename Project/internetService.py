# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from xml.dom.minidom import parseString

def getApi_real_time(date, time, x, y):




    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode({ quote_plus('base_date') : date, quote_plus('base_time') : time, quote_plus('nx') : x, quote_plus('ny') : y, quote_plus('numOfRows') : '10', quote_plus('pageNo') : '1', quote_plus('_type') : 'xml' })

    request = Request(url + queryParams)
    response_body = urlopen(request).read()
    return extractData(response_body)

def extractData(strXml):
    from xml.etree import ElementTree
#    tree = ElementTree.fromstring(strXml)
#    print(strXml)


#    itemElements = tree.getiterator("item") # return list type
#    print(itemElements)
#    for item in itemElements:
#        date = item.find("basedate")
#        time = item.find("basetime")
#        x = item.find("nx")
#        y = item.find("ny")

#        temp = item.find("T1H")
#        humidity = item.find("REH")
    dom = parseString(strXml)
    strXml = dom
    real_time_weather = strXml.childNodes
    response = real_time_weather[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    for item in items:
        data = item.childNodes
        for element in data:
            if element.nodeName == "baseDate":
                date = element.firstChild.nodeValue
            elif element.nodeName == "baseTime":
                time = element.firstChild.nodeValue
            elif element.nodeName == "nx":
                x = element.firstChild.nodeValue
            elif element.nodeName == "ny":
                y = element.firstChild.nodeValue
            elif element.nodeName == "category":
                if element.firstChild.nodeValue == "T1H":
                    for element in data:
                        if element.nodeName == "obsrValue":
                            temp = element.firstChild.nodeValue
                elif element.firstChild.nodeValue == "REH":
                    for element in data:
                        if element.nodeName == "obsrValue":
                            humidity = element.firstChild.nodeValue

    return {"date":date, "time":time, "x":x, "y":y, "temp":temp, "humidity":humidity}
