# -*- coding: cp949 -*-
from urllib.parse import urlencode, quote_plus
from urllib.request import Request, urlopen

url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'
ServiceKey = 'XxhDOcI3Bou6oYWUeSJL9vmmwjnVMuiVtPrHJS8C%2Fki4dFcy7vO%2FtIpHop4rco7U1BBIPI7gdLBoMX1lsC1Bdg%3D%3D'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : ServiceKey, quote_plus('ServiceKey') : ServiceKey, quote_plus('base_date') : '20180528', quote_plus('base_time') : '0600', quote_plus('nx') : '60', quote_plus('ny') : '127', quote_plus('numOfRows') : '10', quote_plus('pageNo') : '1', quote_plus('_type') : 'xml' })

request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
print (response_body)