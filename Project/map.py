# coding: utf8

import json
from urllib.request import urlopen
from urllib.parse import quote
from urllib.parse import urlencode, quote_plus
from transcoord import *

url = 'https://maps.googleapis.com/maps/api/geocode/json?'
key = '&key=AIzaSyDj8yeT04xh5Rox_2Bz3jQdy2QcBmMSMlI'

def SerchGeo(serch):#위도,경도 반환

    apiURL = url+urlencode({quote_plus('address'):serch})+key
    print(apiURL)
    response = urlopen(apiURL).read()
    responseJson =json.loads(response)


    if responseJson['status'] == "OK":
        responselocation = responseJson["results"][0]["geometry"]["location"]
        x, y = grid(responselocation["lat"], responselocation["lng"])   # 위경도를 격자좌표로 변환 후 반환
        # return responselocation["lat"], responselocation["lng"], x, y
        return x, y , responseJson

    else:
        return "error","error" ,"error"




