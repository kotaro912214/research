# coding: UTF-8

import numpy as np
import random
import math
import pprint
import time
import urllib.request, json
import urllib.parse

# read SID from another file for security perspective
def readSID():
  sid_path = '../get_station/sid.txt'
  f = open(sid_path)
  SID = f.read()
  return SID


def makeRequest(api, params):
  request = 'https://api-challenge.navitime.biz/v1s/' + readSID() + api
  i = 0
  for param, value in params.items():
    if (not value):
      continue
    elif (i == 0):
      request += param + '=' + value
    else:
      request += '&' + param + '=' + value
    i += 1
  return request


def getResponse(request):
  response = json.loads(urllib.request.urlopen(request).read())
  return response


KIND_OF_AIP = {'spot_list':'/spot/list?', 'category_list': '/category/list?', 'route': '/route?'}

params = {'category': '', 'coord': '', 'radius': '', 'limit': '', 'datum': '', }
params['category'] = '0817001002' # category code of careco carsharing
params['coord'] = '35.689296,139.702089' # a coord of shinjuku station
params['radius'] = '1800'
params['limit'] = '100'
params['datum'] = 'wgs84'
# word = urllib.parse.quote('港区')

# get the data of the station list
request = makeRequest(KIND_OF_AIP['spot_list'], params)
json_res = getResponse(request)

if (json_res['count']['total'] >= json_res['count']['limit']):
  NUMBER_OF_STATIONS = json_res['count']['limit']
else:
  NUMBER_OF_STATIONS = json_res['count']['total']
spots = json_res['items']
S_coord = []
for spot in spots:
  S_coord.append((spot['coord']['lon'], spot['coord']['lat']))