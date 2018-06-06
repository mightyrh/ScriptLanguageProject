# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from xml.dom.minidom import parseString
from currentTime import*

def makeUrl_real_time_weather(date, time, x, y):
        url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
        ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
        queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
            {quote_plus('base_date'): date, quote_plus('base_time'): time, quote_plus('nx'): x, quote_plus('ny'): y,
             quote_plus('numOfRows'): '10', quote_plus('pageNo'): '1', quote_plus('_type'): 'xml'})
        return url+queryParams

# 구름 양, 비 등 3 ~ 7일까지 오전 오후 예보
# 8 ~ 10일까지 하루 예보
def makeUrl_medium_term_forecast(locationCode, time):   # 중기 기온예보와 지역 코드 다름...
        url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleLandWeather'
        ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
        queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
            {quote_plus('regId'): locationCode, quote_plus('tmFc'): time,
             quote_plus('numOfRows'): '10', quote_plus('pageNo'): '1'})
        return url + queryParams

# 3 ~ 10일까지 최저, 최고기온 예보
def makeUrl_medium_term_temperature(cityCode, time):    # 시간 201806050600 형식으로 정해줘야 함 도시 코드는 문서 참조
    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleTemperature'
    ServiceKey= 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): cityCode, quote_plus('tmFc'): time, #'201707200600',
         quote_plus('pageNo'): '1', quote_plus('numOfRows'): '10'})
    return url + queryParams

# 실시간 광역시, 특별시, 도 별 대기오염 정보
# 대기오염 카테고리 여러가지 확인 할 수 있음
def makeUrl_air_quality_forecast(city, category): # 시, 도를 입력하면 첫번째 원소가 실시간 정보
    #   PM10 미세먼지
    #   PM25 초미세먼지
    #   O3 오존
    #   C0 일산화탄소

    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('numOfRows'): '10', quote_plus('pageNo'): '1',
         quote_plus('sidoName'): city, quote_plus('ver'): '1.3'})
    return url + queryParams


def getApi_real_time_weather(date, time, x, y):
    url = makeUrl_real_time_weather(date, time, x, y)
    print (url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_real_time_weather(response_body)

def getApi_medium_term_forecast(locationCode, time):
    url = makeUrl_medium_term_forecast(locationCode, time)
    print (url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_medium_term_forecast(response_body)

def getApi_medium_term_temperature(cityCode, time):
    url = makeUrl_medium_term_temperature(cityCode, time)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_medium_term_temperature(response_body)

def getApi_air_quality_forecast(city, category):
    url = makeUrl_air_quality_forecast(city, category)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_medium_term_forecast(response_body)

def extractData_real_time_weather(strXml):

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

def extractData_medium_term_forecast(strXml):
    forecast = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
    forecast_index = 0

    dom = parseString(strXml)
    strXml = dom
    medium_term_forecase = strXml.childNodes
    response = medium_term_forecase[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    item = items[0].childNodes

    for element in item:

        if element.nodeName == "wf3Am":
            forecast_index = 0
        elif element.nodeName == "wf3Pm":
            forecast_index = 1
        elif element.nodeName == "wf4Am":
            forecast_index = 2
        elif element.nodeName == "wf4Pm":
            forecast_index = 3
        elif element.nodeName == "wf5Am":
            forecast_index = 4
        elif element.nodeName == "wf5Pm":
            forecast_index = 5
        elif element.nodeName == "wf6Am":
            forecast_index = 6
        elif element.nodeName == "wf6Pm":
            forecast_index = 7
        elif element.nodeName == "wf7Am":
            forecast_index = 8
        elif element.nodeName == "wf7Pm":
            forecast_index = 9
        elif element.nodeName == "wf8":
            forecast_index = 10
        elif element.nodeName == "wf9":
            forecast_index = 11
        elif element.nodeName == "wf10":
            forecast_index = 12
        del forecast[forecast_index]
        forecast.insert(forecast_index, element.firstChild.nodeValue)

    return forecast

def extractData_medium_term_temperature(strXml):
    temperature = ["", "", "", "", "", "", "", "", "", "",
                  "", "", "", "", "", ""]
    temperature_index = 0

    dom = parseString(strXml)
    strXml = dom
    medium_term_temperature = strXml.childNodes
    response = medium_term_temperature[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    item = items[0].childNodes

    for element in item:
        if element.nodeName == "taMin3":
            temperature_index = 0
        elif element.nodeName == "taMax3":
            temperature_index = 1
        elif element.nodeName == "taMin4":
            temperature_index = 2
        elif element.nodeName == "taMax4":
            temperature_index = 3
        elif element.nodeName == "taMin5":
            temperature_index = 4
        elif element.nodeName == "taMax5":
            temperature_index = 5
        elif element.nodeName == "taMin6":
            temperature_index = 6
        elif element.nodeName == "taMax6":
            temperature_index = 7
        elif element.nodeName == "taMin7":
            temperature_index = 8
        elif element.nodeName == "taMax7":
            temperature_index = 9
        elif element.nodeName == "taMin8":
            temperature_index = 10
        elif element.nodeName == "taMax8":
            temperature_index = 11
        elif element.nodeName == "taMin9":
            temperature_index = 12
        elif element.nodeName == "taMax9":
            temperature_index = 13
        elif element.nodeName == "taMin10":
            temperature_index = 14
        elif element.nodeName == "taMax10":
            temperature_index = 15
        del temperature[temperature_index]
        temperature.insert(temperature_index, element.firstChild.nodeValue)

    return temperature

#def extractData_air_quality_forecast(strXml):


def getData_real_time_weather(x, y):
    date, time = nowDateTime()

    data = getApi_real_time_weather(date, time, x, y)
    return data

print(getApi_medium_term_forecast("11B00000", "201806060600"))
print(getApi_medium_term_temperature("11B10101", "201806060600"))