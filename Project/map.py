## coding: utf8
#-*- coding: utf-8 -*-
import json
from urllib.request import urlopen
from io import BytesIO
from urllib.parse import urlencode, quote_plus
from transcoord import *

url = 'https://maps.googleapis.com/maps/api/geocode/json?'
key = '&key=AIzaSyDj8yeT04xh5Rox_2Bz3jQdy2QcBmMSMlI'

def SearchGeo(search):#위도,경도 반환

    apiURL = url+urlencode({quote_plus('address'):search}) +'&language=ko' + key
    print(apiURL)
    response = urlopen(apiURL).read()
    responseJson =json.loads(response)


    if responseJson['status'] == "OK":
        responselocation = responseJson["results"][0]["geometry"]["location"]
        x, y = grid(responselocation["lat"], responselocation["lng"])   # 위경도를 격자좌표로 변환 후 반환
        # return responselocation["lat"], responselocation["lng"], x, y
        cityName = responseJson["results"][0]["address_components"][0]["long_name"]
        return {"x": x, "y": y, "cityName": cityName, "mapdata": responseJson,
                "mapimage": mapimage(responselocation["lat"], responselocation["lng"])}

    else:
        return "error","error" ,"error"


def mapimage(lat, lng):
    url = "https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lng) +"&zoom=13&size=400x400&format=jpg&key=AIzaSyCWJAM-nuDT2BaF08b6VR9dQXn3um7puaA"
    print(url)
    with urlopen(url) as u:
        raw_data = u.read()

    return raw_data
