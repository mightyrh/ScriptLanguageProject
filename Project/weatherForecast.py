from apiService import*
from map import*
def weather_for_today(cityName):
    x, y, null, null = SerchGeo(cityName)
    print(getApi_weather_for_a_day(x, y, "today"))
    print(getData_real_time_weather(x, y))
    print(getApi_medium_term_forecast(cityName))
    print(getApi_medium_term_temperature(cityName))
    print(getApi_air_quality_forecast(cityName))

weather_for_today('서울')