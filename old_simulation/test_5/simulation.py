from pathlib import Path, PureWindowsPath
import csv
import urllib.request, json
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
import time
from myfunc import my_round

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
    self.base_path = PureWindowsPath(Path.cwd())

  def read_sid(self):
    sid_path = self.base_path / 'sid.txt'
    f = open(sid_path)
    SID = f.read()
    return SID


  def make_request(self, api, params):
    request = 'https://api-challenge.navitime.biz/v1s/' + self.read_sid() + api
    url_params = urllib.parse.urlencode(params)
    request += url_params
    return request


  def get_response(self, request):
    try:
      response = json.loads(urllib.request.urlopen(request).read())
    except urllib.error.HTTPError as e:
      print('** error **', 'got HTTPerror, invalid request was issued')
      print('code:', e.code)
      exit()
    except urllib.error.HTTPError as e:
      print('** error **', 'We failed to reach a server.')
      print('reason:', e.reason)
      exit()
    else:
      return response


  def write_matrix(self, matrix, path):
    try:
      file = open(path, 'x', encoding='utf-8')
    except FileExistsError:
      print(path, ' has already made')
    else:
      writer = csv.writer(file, lineterminator='\n')
      desc = 'making ' + path.name
      writer.writerows(tqdm(matrix, desc=desc))
      file.close()


  def write_const(self):
    self.CONSTS = [
      ['NUMBER_OF_STATIONS', self.NUMBER_OF_STATIONS],
      ['NUMBER_OF_EMPLOYEES', self.NUMBER_OF_EMPLOYEES],
      ['TIME', self.TIME],
      ['C_IN', self.C_IN],
      ['C_OUT', self.C_OUT],
      ['C_E_FULL', self.C_E_FULL],
      ['PRICE_PER_15', self.PRICE_PER_15],
      ['FUEL_CONSUMPTION', self.FUEL_CONSUMPTION],
      ['C_E_DAY', self.C_E_DAY],
    ]
    self.write_matrix(self.CONSTS, self.base_path / ('const_' + str(self.NUMBER_OF_STATIONS) + '.csv'))


  def make_stations_coord(self):
    file_name =  'S_coord_' + str(self.NUMBER_OF_STATIONS) + '.csv'
    if (not (Path.cwd() / file_name).exists()):
      # set the params for spot list request
      params_spot = {'category': '', 'coord': '', 'radius': '', 'limit': '', 'datum': ''}
      params_spot['category'] = '0817001002' # category code of careco carsharing
      params_spot['coord'] = '35.689296,139.702089' # a coord of shinjuku station
      params_spot['radius'] = '100000'
      params_spot['limit'] = str(self.NUMBER_OF_STATIONS)
      params_spot['datum'] = 'tokyo'

      # get the data of the station list
      request = self.make_request(self.KIND_OF_AIP['spot_list'], params_spot)
      json_res = self.get_response(request)

      spots = json_res['items']
      S_info = []
      S_coord = []
      for spot in spots:
        S_coord.append((spot['coord']['lat'], spot['coord']['lon']))
        S_info.append([spot['name'], spot['coord']['lat'], spot['coord']['lon']])
      self.write_matrix(S_coord, self.base_path / ('S_coord_' + str(self.NUMBER_OF_STATIONS) + '.csv'))
      self.write_matrix(S_info, self.base_path / ('S_info_' + str(self.NUMBER_OF_STATIONS) + '.csv'))
    else:
      print('** error **', Path.cwd() / 'S_coord_?.csv', 'has already existed')


  def make_stations_links(self):
    if (not (Path.cwd() / 'station_links.csv').exists()):
      links = []
      for i in tqdm(range(1, 51), desc='scraping...'):
        if (i == 1):
          url = 'https://www.navitime.co.jp/category/0817001002/13'
        else:
          url = 'https://www.navitime.co.jp/category/0817001002/13/?page=' + str(i)
        time.sleep(1)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        spot_names = soup.find_all(class_="spot_name")
        for spot_name in spot_names:
          links.append(['https:' + spot_name.a.get("href"), spot_name.a.string])
      self.write_matrix(links, self.base_path / 'station_links.csv')
    else:
      print('** error **', Path.cwd() / 'station_links.csv', 'has already existed')

  
  def make_available_cars(self):
    if (not (Path.cwd() / 'station_links.csv').exists()):
      print('** error ** there is no file about station links.')
    elif ((Path.cwd() / 'available_cars.csv').exists()):
      print('** error ** available_cars.csv has already existed')
    else:
      csv_file = open(self.base_path / 'station_links.csv', 'r', encoding='utf-8')
      datas = list(csv.reader(csv_file, delimiter=","))
      avail_cars = []
      for i in tqdm(range(len(datas)), desc='scraiping...'):
        url = datas[i][0]
        time.sleep(1)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        avail_car = soup.find(class_="detail_contents").find_all("dd")[2].string[:-1]
        avail_cars.append((datas[i][1], avail_car))
      self.write_matrix(avail_cars, self.base_path / 'available_cars.csv')





if (__name__ == '__main__'):
  print('you have to import this file from another file')