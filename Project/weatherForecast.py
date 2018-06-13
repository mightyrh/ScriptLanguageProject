from apiService import*
from map import*
def weather_for_today(cityName):
    print(getApi_weather_for_a_day(cityName, "today"))
    print(getApi_medium_term_forecast(cityName))
    print(getApi_medium_term_temperature(cityName))
    print(getApi_air_quality_forecast(cityName))

weather_for_today('서울')