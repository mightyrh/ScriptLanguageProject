from apiService import*
from map import*
def weather_for_today(x, y):
    targetTime = ['0600', '0900', '1200', '1500', '1800', '2100', '0000', '0300']
    data =  getApi_weather_for_a_day(x, y, "today")

    PTY = ""
    SKY = ""
    TMN = 0
    TMX = 0

    forecastList = []
#    forecastList.append("날짜: " + year + "년 " + month + "월 " + day + "일" + "\n")

    for time in targetTime:
        if data[time]['PTY'] == '0':
            PTY = "비 안옴"
        elif data[time]['PTY'] == '1':
            PTY = "비"
        elif data[time]['PTY'] == '2':
            PTY = "진눈깨비"
        elif data[time]['PTY'] == '3':
            PTY = "눈"

        if data[time]['SKY'] == '1':
            SKY = "맑음"
        elif data[time]['SKY'] == '2':
            SKY = "구름조금"
        elif data[time]['SKY'] == '3':
            SKY = "구름많음"
        elif data[time]['SKY'] == '4':
            SKY = "흐림"

        forecastList.append(time + "시:\n" + "강수확률: " + data[time]["POP"] + "%\n" \
                   + "강수형태: " + PTY + "\n습도 :" + data[time]['REH'] + "%\n" \
                   + "하늘상태: " + SKY + "\n기온: " + data[time]['T3H'] + "도\n\n")
        if data[time]['TMN'] != -999:
            TMN = data[time]['TMN']
        if data[time]['TMX'] != -999:
            TMX = data[time]['TMX']
        minmaxTemperature = "\n최저기온: " + str(TMN) + "도" + "\n최고기온: " + str(TMX) + "도"

    resultForecast = ""
    for forecast in forecastList:
        resultForecast += forecast
    return resultForecast + minmaxTemperature



#weather_for_today('서울')

#print(getApi_medium_term_forecast(cityName))
#print(getApi_medium_term_temperature(cityName))
#print(getApi_air_quality_forecast(cityName))