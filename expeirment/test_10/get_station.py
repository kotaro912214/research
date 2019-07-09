# coding: UTF-8

import numpy as np
import random
import time
import urllib.request, json
import urllib.parse
import csv

# read SID from another file for security perspective
def readSID():
  sid_path = '../../get_station/sid.txt'
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


def writeMatrix(matrix, path):
  with open(path, 'w', encoding='utf-8') as file:
      writer = csv.writer(file, lineterminator='\n')
      writer.writerows(matrix)

def writeConst(const_name, const_value):
  f = open('./const.csv', 'a', encoding='utf-8')
  f.write(const_name + ',' + str(const_value) + '\n')


KIND_OF_AIP = {'spot_list':'/spot/list?', 'category_list': '/category/list?', 'route': '/route?'}

# set the params for spot list request
params_spot = {'category': '', 'coord': '', 'radius': '', 'limit': '', 'datum': ''}
params_spot['category'] = '0817001002' # category code of careco carsharing
params_spot['coord'] = '35.689296,139.702089' # a coord of shinjuku station
params_spot['radius'] = '1800'
params_spot['limit'] = '10'
params_spot['datum'] = 'tokyo'
# word = urllib.parse.quote('港区')

# get the data of the station list
request = makeRequest(KIND_OF_AIP['spot_list'], params_spot)
json_res = getResponse(request)

# set the number of stations const. and coord of stations matrix
if (json_res['count']['total'] >= json_res['count']['limit']):
  NUMBER_OF_STATIONS = json_res['count']['limit']
else:
  NUMBER_OF_STATIONS = json_res['count']['total']
spots = json_res['items']
S_info = []
S_coord = []
for spot in spots:
  S_coord.append((spot['coord']['lat'], spot['coord']['lon']))
  S_info.append([spot['name'], spot['coord']['lat'], spot['coord']['lon']])



# set the params for spot list request
params_route = {'walk': '', 'start': '', 'goal': '', 'order': '', 'car-fuel': ''}
params_route['car'] = 'only'
params_route['order'] = 'total_distance'
# 35km per L
FUEL_CONSUMPTION = 35
params_route['car-fuel'] = str(FUEL_CONSUMPTION)
Distance = np.zeros((NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
T_trans = np.zeros((NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
for i in range(NUMBER_OF_STATIONS - 1):
  for j in range(i + 1, NUMBER_OF_STATIONS):
    # time.sleep(1)
    if (S_coord[i] != S_coord[j]):
      params_route['start'] = str(S_coord[i][0]) + ',' + str(S_coord[i][1])
      params_route['goal'] = str(S_coord[j][0]) + ',' + str(S_coord[j][1])
      time.sleep(0.65)
      request = makeRequest(KIND_OF_AIP['route'], params_route)
      response = getResponse(request)
      Distance[i][j] = response['items'][0]['summary']['move']['distance']
      Distance[j][i] = response['items'][0]['summary']['move']['distance']
      T_trans[i][j] = response['items'][0]['summary']['move']['time']
      T_trans[j][i] = response['items'][0]['summary']['move']['time']
    else:
      Distance[i][j] = 0
      T_trans[i][j] = 0

writeMatrix(S_coord, './s_coord.csv')
writeMatrix(Distance, './distance.csv')
writeMatrix(T_trans, './t_trans.csv')
writeMatrix(S_info, './s_info.csv')
writeConst('NUMBER_OF_STATIONS', NUMBER_OF_STATIONS)
writeConst('FUEL_CONSUMPTION', FUEL_CONSUMPTION)

# define the time which transportation between station i to j will take
# T_distance = [
#   [0, 5, 10, 7, 5],
#   [5, 0, 18, 13, 10],
#   [10, 18, 0, 19, 4],
#   [7, 13, 19, 0, 21],
#   [5, 10, 4, 21, 0]
# ]