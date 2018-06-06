# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from xml.dom.minidom import parseString
from currentTime import*

def makeUrl_real_time_weather2(date, base_time, x, y):
    # base_time 0200 0500 0800 1100 1400 1700 2000 2300 ���� 4�ð� �ĸ� ������
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode({
                                   quote_plus('base_date'): date, quote_plus('base_time'): base_time,
                                   quote_plus('nx'): x, quote_plus('ny'): y, quote_plus('numOfRows'): '10',
                                   quote_plus('pageNo'): '1', quote_plus('_type'): 'xml'})

def makeUrl_real_time_weather(date, time, x, y):
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('base_date'): date, quote_plus('base_time'): time, quote_plus('nx'): x, quote_plus('ny'): y,
         quote_plus('numOfRows'): '10', quote_plus('pageNo'): '1', quote_plus('_type'): 'xml'})
    return url+queryParams

# ���� ��, �� �� 3 ~ 7�ϱ��� ���� ���� ����
# 8 ~ 10�ϱ��� �Ϸ� ����
def makeUrl_medium_term_forecast(locationCode, time):   # �߱� ��¿����� ���� �ڵ� �ٸ�...
        url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleLandWeather'
        ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
        queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
            {quote_plus('regId'): locationCode, quote_plus('tmFc'): time,
             quote_plus('numOfRows'): '1', quote_plus('pageNo'): '1'})
        return url + queryParams

# 3 ~ 10�ϱ��� ����, �ְ��� ����
def makeUrl_medium_term_temperature(cityCode, time):    # �ð� 201806050600 �������� ������� �� ���� �ڵ�� ���� ����
    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleTemperature'
    ServiceKey= 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): cityCode, quote_plus('tmFc'): time, #'201707200600',
         quote_plus('pageNo'): '1', quote_plus('numOfRows'): '1'})
    return url + queryParams

# �ǽð� ������, Ư����, �� �� ������ ����
# ������ ī�װ� �������� Ȯ�� �� �� ����
def makeUrl_air_quality_forecast(category): # ��, ���� �Է��ϸ� ù��° ���Ұ� �ǽð� ����
    #   PM10 �̼�����
    #   PM25 �ʹ̼�����
    #   O3 ����
    #   C0 �ϻ�ȭź��

    url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('numOfRows') : '1', quote_plus('pageNo') : '1', quote_plus('itemCode') : category,
         quote_plus('dataGubun') : 'HOUR', quote_plus('searchCondition') : 'MONTH' })
    return url + queryParams

########################################################################
def getApi_real_time_weather2(date, base_time, x, y):
    url = makeUrl_real_time_weather2(date, base_time, x, y)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_real_time_weather2(response_body)

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

def getApi_air_quality_forecast(category):
    url = makeUrl_air_quality_forecast(category)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_air_quality_forecast(response_body)


########################################################################
def extractData_real_time_weather2(strXml):
    dom = parseString(strXml)
    strXml = dom
    real_time_weather = strXml.childNodes
    response = real_time_weather[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    

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
    forecast = {'wf3Am' : "", 'wf3Pm' : "", 'wf4Am' : "", 'wf4Pm' : "",
                'wf5Am' : "", 'wf5Pm' : "", 'wf6Am' : "", 'wf6Pm' : "",
                'wf7Am' : "", 'wf7Pm' : "", 'wf8' : "", 'wf9' : "", 'wf10' : ""}

    dom = parseString(strXml)
    strXml = dom
    medium_term_forecase = strXml.childNodes
    response = medium_term_forecase[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    item = items[0].childNodes

    for element in item:
        forecast[element.nodeName] = element.firstChild.nodeValue

    return forecast

def extractData_medium_term_temperature(strXml):
    temperature = {'taMin3' : -999, 'taMax3' : -999, 'taMin4' : -999, 'taMax4' : -999,
                   'taMin5' : -999, 'taMax5' : -999, 'taMin6' : -999, 'taMax6' : -999,
                   'taMin7' : -999, 'taMax7' : -999, 'taMin8' : -999, 'taMax8' : -999,
                   'taMin9' : -999, 'taMax9' : -999, 'taMin10' : -999, 'taMax10' : -999}

    dom = parseString(strXml)
    strXml = dom
    medium_term_temperature = strXml.childNodes
    response = medium_term_temperature[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    item = items[0].childNodes

    for element in item:
        temperature[element.nodeName] = element.firstChild.nodeValue

    return temperature

def extractData_air_quality_forecast(strXml):
    air_quality = {'seoul' : -999, 'busan' : -999, 'daegu' : -999,
                   'incheon' : -999, 'gwangju' : -999, 'daejeon' : -999,
                   'ulsan' : -999, 'gyeonggi' : -999, 'gangwon' : -999,
                   'chungbuk' : -999, 'chungnam' : -999, 'jeonbuk' : -999,
                   'jeonnam' : -999,'gyeongbuk' : -999, 'gyeongnam' : -999,
                   'jeju' : -999, 'sejong' : -999}

    dom = parseString(strXml)
    strXml = dom
    medium_term_temperature = strXml.childNodes
    response = medium_term_temperature[0].childNodes
    body = response[3].childNodes
    items = body[1].childNodes
    item = items[1].childNodes

    for element in item:
        if element.nodeName in air_quality:
            air_quality[element.nodeName] = element.firstChild.nodeValue

    return air_quality

def getData_real_time_weather(x, y):
    date, time = nowDateTime()

    data = getApi_real_time_weather(date, time, x, y)
    return data

print(getData_real_time_weather("60", "127"))
print(getApi_medium_term_forecast("11B00000", "201806060600"))
print(getApi_medium_term_temperature("11B10101", "201806060600"))
print(getApi_air_quality_forecast("PM10"))