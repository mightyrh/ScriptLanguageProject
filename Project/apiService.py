# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen
from xml.dom.minidom import parseString
from Time import*
from map import*

# date 는 전날로 입력 받아야 함. 전날 2000 부터 82개 받아오면 오늘 하루 치임
# 1페이지는 오늘
# 2페이지는 내일
def makeUrl_weather_for_a_day(x, y, day):
    # base_time 0200 0500 0800 1100 1400 1700 2000 2300 각각 4시간 후를 예보함

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

# 구름 양, 비 등 3 ~ 7일까지 오전 오후 예보
# 8 ~ 10일까지 하루 예보
def makeUrl_medium_term_forecast(locationCode):   # 중기 기온예보와 지역 코드 다름...
    time = dateCalculate('0000')

    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleLandWeather'
    ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): locationCode, quote_plus('tmFc'): time.strftime('%Y%m%d') + '0600',
         quote_plus('numOfRows'): '1', quote_plus('pageNo'): '1'})
    return url + queryParams

# 3 ~ 10일까지 최저, 최고기온 예보
def makeUrl_medium_term_temperature(cityCode):    # 시간 201806050600 형식으로 정해줘야 함 도시 코드는 문서 참조
    time = dateCalculate('0000')
    url = 'http://newsky2.kma.go.kr/service/MiddleFrcstInfoService/getMiddleTemperature'
    ServiceKey= 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
    queryParams = '?' + 'serviceKey=' + ServiceKey + '&' + urlencode(
        {quote_plus('regId'): cityCode, quote_plus('tmFc'): time.strftime('%Y%m%d') + '0600', #'201707200600',
         quote_plus('pageNo'): '1', quote_plus('numOfRows'): '1'})
    return url + queryParams

# 실시간 광역시, 특별시, 도 별 대기오염 정보
# 대기오염 카테고리 여러가지 확인 할 수 있음
def makeUrl_air_quality_forecast(category): # 시, 도를 입력하면 첫번째 원소가 실시간 정보
    #   PM10 미세먼지
    #   PM25 초미세먼지
    #   O3 오존
    #   C0 일산화탄소

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
# 0200 시 이전에는 전날 기준으로 가져오고
# 0200 시 이후로는 오늘 기준으로 가져옴
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
        air_quality = '좋음'
    elif 30 < int(PM10_Level) <= 80:
        air_quality = '보통'
    elif 80 < int(PM10_Level) <= 150:
        air_quality = '나쁨'
    elif 150 < int(PM10_Level):
        air_quality = '매우나쁨'

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
    if cityName == '서울특별시':return '11B10101'
    elif cityName == '인천광역시':return '11B20201'
    elif cityName == '수원시':return '11B20601'
    elif cityName == '파주시':return '11B20305'
    elif cityName == '춘천시':return '11D10301'
    elif cityName == '원주시':return '11D10401'
    elif cityName == '강릉시':return '11D20501'
    elif cityName == '대전시':return '11C20401'
    elif cityName == '서산시':return '11C20101'
    elif cityName == '세종시':return '11C20404'
    elif cityName == '청주시':return '11C10301'
    elif cityName == '제주시':return '11G00201'
    elif cityName == '서귀포시':return '11G00401'
    elif cityName == '광주광역시':return '11F20501'
    elif cityName == '목포시':return '21F20801'
    elif cityName == '여수시':return '11F20401'
    elif cityName == '전주시':return '11F10201'
    elif cityName == '군산시':return '21F10501'
    elif cityName == '부산광역시':return '11H20201'
    elif cityName == '울산광역시':return '11H20101'
    elif cityName == '창원시':return '11H20301'
    elif cityName == '대구광역시':return '11H10701'
    elif cityName == '안동시':return '11H10501'
    elif cityName == '포항시':return '11H10201'

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
    if cityName == '서울특별시':cityName_In_Korean = 'seoul'
    elif cityName == '부산광역시':cityName_In_Korean = 'busan'
    elif cityName == '대구광역시':cityName_In_Korean = 'daegu'
    elif cityName == '인천광역시':cityName_In_Korean = 'incheon'
    elif cityName == '광주광역시':cityName_In_Korean = 'gwangju'
    elif cityName == '대구광역시':cityName_In_Korean = 'daegu'
    elif cityName == '울산광역시':cityName_In_Korean = 'ulsan'
    elif cityName == '경기도':cityName_In_Korean = 'gyeonggi'
    elif cityName == '강원도':cityName_In_Korean = 'gangwon'
    elif cityName == '충청북도':cityName_In_Korean = 'chungbuk'
    elif cityName == '충청남도':cityName_In_Korean = 'chungnam'
    elif cityName == '전라북도':cityName_In_Korean = 'jeonbuk'
    elif cityName == '전라남도':cityName_In_Korean = 'jeonnam'
    elif cityName == '경상북도':cityName_In_Korean = 'gyeongbuk'
    elif cityName == '경상남도':cityName_In_Korean = 'gyeongnam'
    elif cityName == '제주도':cityName_In_Korean = 'jeju'
    #elif cityName == '세종':cityName_In_Korean = 'sejong'

    return cityName_In_Korean

#print(getApi_weather_for_a_day('서울', "today"))
#print(getApi_real_time_weather('서울'))
#print(getData_real_time_weather("60", "127"))
#print(getApi_medium_term_forecast('서울'))
#print(getApi_medium_term_temperature('서울'))
#print(getApi_air_quality_forecast('서울'))
