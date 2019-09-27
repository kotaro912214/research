import get_station
from pathlib import Path, PureWindowsPath
import csv
import urllib.request, json
import urllib.parse

class Simulation():

  def __init__(self, params={
    'NUMBER_OF_EMPLOYEES': 4,
    'TIME': 60 * 8,
    'C_IN': 100,
    'C_OUT': 205,
    'C_E_FULL': 10000,
    'PRICE_PER_15': 205,
    'FUEL_CONSUMPTION': 35,
    'NUMBER_OF_STATIONS': 5
  }):
    self.NUMBER_OF_EMPLOYEES = params['NUMBER_OF_EMPLOYEES']
    self.TIME = params['TIME']
    self.C_IN = params['C_IN']
    self.C_OUT  = params['C_OUT']
    self.C_E_FULL  = params['C_E_FULL']
    self.PRICE_PER_15  = params['PRICE_PER_15']
    self.FUEL_CONSUMPTION  = params['FUEL_CONSUMPTION']
    self.NUMBER_OF_STATIONS  = params['NUMBER_OF_STATIONS']
    self.C_E_DAY = self.C_E_FULL * (self.TIME / 8 * 60)
    self.KIND_OF_AIP = {'spot_list':'/spot/list?', 'category_list': '/category/list?', 'route': '/route?'}

  def readSID(self):
    base_path = PureWindowsPath(Path.cwd())
    sid_path = base_path / 'sid.txt'
    print(sid_path)
    f = open(sid_path)
    SID = f.read()
    return SID


  def makeRequest(self, api, params):
    request = 'https://api-challenge.navitime.biz/v1s/' + self.readSID() + api
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


  def getResponse(self, request):
    response = json.loads(urllib.request.urlopen(request).read())
    return response


  def writeMatrix(self, matrix, path):
    with open(path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(matrix)

  def writeConst(self, const_name, const_value):
    f = open('./const.csv', 'a', encoding='utf-8')
    f.write(const_name + ',' + str(const_value) + '\n')

  def makeScoord(self):
    
    # set the params for spot list request
    params_spot = {'category': '', 'coord': '', 'radius': '', 'limit': '', 'datum': ''}
    params_spot['category'] = '0817001002' # category code of careco carsharing
    params_spot['coord'] = '35.689296,139.702089' # a coord of shinjuku station
    params_spot['radius'] = '100000'
    params_spot['limit'] = str(self.NUMBER_OF_STATIONS)
    params_spot['datum'] = 'tokyo'

    # get the data of the station list
    request = self.makeRequest(self.KIND_OF_AIP['spot_list'], params_spot)
    json_res = self.getResponse(request)

    spots = json_res['items']
    S_info = []
    S_coord = []
    for spot in spots:
      S_coord.append((spot['coord']['lat'], spot['coord']['lon']))
      S_info.append([spot['name'], spot['coord']['lat'], spot['coord']['lon']])
    base_path = PureWindowsPath(Path.cwd())
    self.writeMatrix(S_coord, base_path / ('S_coord' + str(self.NUMBER_OF_STATIONS)))


if (__name__ == '__main__'):
  print('hs')