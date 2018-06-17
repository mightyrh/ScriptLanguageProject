# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from xml.dom.minidom import parseString
from Time import*
from map import*

# date �� ������ �Է� �޾ƾ� ��. ���� 2000 ���� 82�� �޾ƿ��� ���� �Ϸ� ġ��
# 1�������� ����
# 2�������� ����
def makeUrl_weather_for_a_day(x, y, day):
    # base_time 0200 0500 0800 1100 1400 1700 2000 2300 ���� 4�ð� �ĸ� ������

    if day == 'today':
        pageNo = 1
    elif day == 'tomorrow':
        pageNo = 2

    base_date = dateCalculate('0200').strftime('%Y%m%d')

    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode({
                                   quote_plus('base_date'): base_date, quote_plus('base_time'): '0200',
                                   quote_plus('nx'): x, quote_plus('ny'): y, quote_plus('numOfRows'): '82',
                                   quote_plus('pageNo'): pageNo, quote_plus('_type'): 'xml'})
    return url+queryParams

def makeUrl_real_time_weather(x, y):
    date, time = nowDateTime()

    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('base_date'): date, quote_plus('base_time'): time, quote_plus('nx'): x, quote_plus('ny'): y,
         quote_plus('numOfRows'): '10', quote_plus('pageNo'): '1', quote_plus('_type'): 'xml'})
    return url+queryParams

# ���� ��, �� �� 3 ~ 7�ϱ��� ���� ���� ����
# 8 ~ 10�ϱ��� �Ϸ� ����
def makeUrl_medium_term_forecast(locationCode):   # �߱� ��¿����� ���� �ڵ� �ٸ�...
    time = dateCalculate('0000')

    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleLandWeather'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): locationCode, quote_plus('tmFc'): time.strftime('%Y%m%d') + '0600',
         quote_plus('numOfRows'): '1', quote_plus('pageNo'): '1'})
    return url + queryParams

# 3 ~ 10�ϱ��� ����, �ְ��� ����
def makeUrl_medium_term_temperature(cityCode):    # �ð� 201806050600 �������� ������� �� ���� �ڵ�� ���� ����
    time = dateCalculate('0000')
    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleTemperature'
    ServiceKey= 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): cityCode, quote_plus('tmFc'): time.strftime('%Y%m%d') + '0600', #'201707200600',
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
def getApi_weather_for_a_day(x, y, day):
    url = makeUrl_weather_for_a_day(x, y, day)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_weather_for_a_day(response_body)

def getApi_real_time_weather(x, y):
    url = makeUrl_real_time_weather(x, y)
    print (url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_real_time_weather(response_body)

def getApi_medium_term_forecast(cityName):
    locationCode = getLocationCode_SKY(cityName)
    url = makeUrl_medium_term_forecast(locationCode)
    print (url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_medium_term_forecast(response_body)

def getApi_medium_term_temperature(cityName):
    cityCode = getLocationCode(cityName)
    url = makeUrl_medium_term_temperature(cityCode)
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_medium_term_temperature(response_body)

def getApi_air_quality_forecast(cityName):
    url = makeUrl_air_quality_forecast('PM10')
    print(url)
    request = Request(url)
    response_body = urlopen(request).read()
    return extractData_air_quality_forecast(response_body, cityName)

########################################################################
# 0200 �� �������� ���� �������� ��������
# 0200 �� ���ķδ� ���� �������� ������
def extractData_weather_for_a_day(strXml):
    forecast = returnDayCat()

    dom = parseString(strXml)
    strXml = dom
    real_time_weather = strXml.childNodes
    response = real_time_weather[0].childNodes
    body = response[1].childNodes
    items = body[0].childNodes
    for item in items:
        data = item.childNodes
        category = data[2].firstChild.nodeValue
        if category == 'POP' or category == 'PTY' or category == 'REH' or category == 'SKY' or category == 'T3H' or category == 'TMN' or category == 'TMX':
            if int(data[3].firstChild.nodeValue) == int(data[0].firstChild.nodeValue):
                forecast[data[4].firstChild.nodeValue][data[2].firstChild.nodeValue] = data[5].firstChild.nodeValue
            elif int(data[3].firstChild.nodeValue) == int(data[0].firstChild.nodeValue) + 1:
                forecast[data[4].firstChild.nodeValue][data[2].firstChild.nodeValue] = data[5].firstChild.nodeValue

    return forecast




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

def extractData_air_quality_forecast(strXml, location):
    location = getCityName_In_English(location)

    dom = parseString(strXml)
    strXml = dom
    medium_term_temperature = strXml.childNodes
    response = medium_term_temperature[0].childNodes
    body = response[3].childNodes
    items = body[1].childNodes
    item = items[1].childNodes

    for element in item:
        if element.nodeName == location:
            PM10_Level = element.firstChild.nodeValue
            #air_quality[element.nodeName] = element.firstChild.nodeValue

    if  0 <= int(PM10_Level) <= 30:
        air_quality = '����'
    elif 30 < int(PM10_Level) <= 80:
        air_quality = '����'
    elif 80 < int(PM10_Level) <= 150:
        air_quality = '����'
    elif 150 < int(PM10_Level):
        air_quality = '�ſ쳪��'

    return PM10_Level, air_quality

def returnDayCat():
    return {'0600':returnCat(), '0900':returnCat(),
            '1200':returnCat(), '1500':returnCat(),
            '1800':returnCat(), '2100':returnCat(),
            '0000':returnCat(), '0300':returnCat()}

def returnCat():
    return {'POP': -999, 'PTY': -999, 'REH': -999, 'SKY': -999,
            'T3H': -999, 'TMN': -999, 'TMX': -999}

def getLocationCode(cityName):
    if cityName == '����Ư����':return '11B10101'
    elif cityName == '��õ������':return '11B20201'
    elif cityName == '������':return '11B20601'
    elif cityName == '���ֽ�':return '11B20305'
    elif cityName == '��õ��':return '11D10301'
    elif cityName == '���ֽ�':return '11D10401'
    elif cityName == '������':return '11D20501'
    elif cityName == '������':return '11C20401'
    elif cityName == '�����':return '11C20101'
    elif cityName == '������':return '11C20404'
    elif cityName == 'û�ֽ�':return '11C10301'
    elif cityName == '���ֽ�':return '11G00201'
    elif cityName == '��������':return '11G00401'
    elif cityName == '���ֱ�����':return '11F20501'
    elif cityName == '������':return '21F20801'
    elif cityName == '������':return '11F20401'
    elif cityName == '���ֽ�':return '11F10201'
    elif cityName == '�����':return '21F10501'
    elif cityName == '�λ걤����':return '11H20201'
    elif cityName == '��걤����':return '11H20101'
    elif cityName == 'â����':return '11H20301'
    elif cityName == '�뱸������':return '11H10701'
    elif cityName == '�ȵ���':return '11H10501'
    elif cityName == '���׽�':return '11H10201'

def getLocationCode_SKY(cityName):
    cityCode = getLocationCode(cityName)
    cityCode_List = list(cityCode)
    strCode4 = ''
    strCode3 = ''
    for c in cityCode_List[0:4]:
        strCode4 += c
    for c in cityCode_List[0:3]:
        strCode3 += c
    if strCode3 == '11B':locationCode = '11B00000'
    elif strCode4 == '11D1':locationCode = '11D10000'
    elif strCode4 == '11D2':locationCode = '11D20000'
    elif strCode4 == '11C1':locationCode = '11C10000'
    elif strCode4 == '11C2':locationCode = '11C20000'
    elif strCode4 == '11F2':locationCode = '11F20000'
    elif strCode4 == '11F1':locationCode = '11F10000'
    elif strCode4 == '11H1':locationCode = '11H10000'
    elif strCode4 == '11H2':locationCode = '11H20000'
    elif strCode3 == '11G':locationCode = '11G0000'

    return locationCode

def getCityName_In_English(cityName):
    if cityName == '����Ư����':cityName_In_Korean = 'seoul'
    elif cityName == '�λ걤����':cityName_In_Korean = 'busan'
    elif cityName == '�뱸������':cityName_In_Korean = 'daegu'
    elif cityName == '��õ������':cityName_In_Korean = 'incheon'
    elif cityName == '���ֱ�����':cityName_In_Korean = 'gwangju'
    elif cityName == '�뱸������':cityName_In_Korean = 'daegu'
    elif cityName == '��걤����':cityName_In_Korean = 'ulsan'
    elif cityName == '��⵵':cityName_In_Korean = 'gyeonggi'
    elif cityName == '������':cityName_In_Korean = 'gangwon'
    elif cityName == '��û�ϵ�':cityName_In_Korean = 'chungbuk'
    elif cityName == '��û����':cityName_In_Korean = 'chungnam'
    elif cityName == '����ϵ�':cityName_In_Korean = 'jeonbuk'
    elif cityName == '���󳲵�':cityName_In_Korean = 'jeonnam'
    elif cityName == '���ϵ�':cityName_In_Korean = 'gyeongbuk'
    elif cityName == '��󳲵�':cityName_In_Korean = 'gyeongnam'
    elif cityName == '���ֵ�':cityName_In_Korean = 'jeju'
    #elif cityName == '����':cityName_In_Korean = 'sejong'

    return cityName_In_Korean

#print(getApi_weather_for_a_day('����', "today"))
#print(getApi_real_time_weather('����'))
#print(getData_real_time_weather("60", "127"))
#print(getApi_medium_term_forecast('����'))
#print(getApi_medium_term_temperature('����'))
#print(getApi_air_quality_forecast('����'))
