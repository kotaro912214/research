from pathlib import Path, PureWindowsPath
import csv
import urllib.request
import urllib.json
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
    })
    if (params['NUMBER_OF_STATIONS'] > 1000):
        print('number of stations must be less than 1000')
        print('so we use 1000 as the const.')
        params['NUMBER_OF_STATIONS'] = 1000
    self.NUMBER_OF_EMPLOYEES = params['NUMBER_OF_EMPLOYEES']
    self.TIME = params['TIME']
    self.C_IN = params['C_IN']
    self.C_OUT = params['C_OUT']
    self.C_E_FULL = params['C_E_FULL']
    self.PRICE_PER_15 = params['PRICE_PER_15']
    self.FUEL_CONSUMPTION = params['FUEL_CONSUMPTION']
    self.NUMBER_OF_STATIONS = params['NUMBER_OF_STATIONS']
    self.C_E_DAY = self.C_E_FULL * (self.TIME / 8 * 60)
    self.KIND_OF_AIP = {
        'spot_list': '/spot/list?',
        'category_list': '/category/list?',
        'route': '/route?'
    }
    self.base_path = PureWindowsPath(Path.cwd())

    def read_sid(self):
        sid_path = self.base_path / 'sid.txt'
        f = open(sid_path)
        SID = f.read()
        return SID

    def make_request(self, api, params):
        base_url = 'https://api-challenge.navitime.biz/v1s/'
        request = base_url + self.read_sid() + api
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
        self.write_matrix(
            self.CONSTS,
            self.base_path / ('const_' + str(self.NUMBER_OF_STATIONS) + '.csv')
        )

    def make_stations_coord(self):
        file_name = 'stations_coord_' + str(self.NUMBER_OF_STATIONS) + '.csv'
        if (not (Path.cwd() / file_name).exists()):
            # set the params for spot list request
            params_spot = {
                'category': '',
                'coord': '',
                'radius': '',
                'limit': '',
                'datum': ''
            }
            # category code of careco carsharing
            params_spot['category'] = '0817001002'
            # a coord of shinjuku station
            params_spot['coord'] = '35.689296,139.702089'
            params_spot['radius'] = '100000'
            params_spot['limit'] = str(self.NUMBER_OF_STATIONS)
            params_spot['datum'] = 'tokyo'

            # get the data of the station list
            request = self.make_request(
                self.KIND_OF_AIP['spot_list'],
                params_spot
            )
            json_res = self.get_response(request)

            spots = json_res['items']
            stations_info = []
            stations_coord = []
            for spot in spots:
                stations_coord.append((
                    spot['coord']['lat'],
                    spot['coord']['lon']
                ))
                stations_info.append([
                    spot['name'],
                    spot['coord']['lat'],
                    spot['coord']['lon']
                ])
            self.write_matrix(
                stations_coord,
                self.base_path /
                ('stations_coord_' + str(self.NUMBER_OF_STATIONS) + '.csv')
            )
            self.write_matrix(
                stations_info,
                self.base_path /
                ('stations_info_' + str(self.NUMBER_OF_STATIONS) + '.csv')
            )
        else:
            print(
                '** error **',
                Path.cwd() / 'stations_coord_?.csv or',
                Path.cwd() / 'stations_info_?.csv'
                'has already existed'
            )

    def make_stations_link(self):
        file_name = 'stations_link_' + str(self.NUMBER_OF_STATIONS) + '.csv'
        if (not (Path.cwd() / file_name).exists()):
            links = []
            n = self.NUMBER_OF_STATIONS // 20
            for i in tqdm(range(1, n + 1), desc='scraping...'):
                url = 'https://www.navitime.co.jp/category/0817001002/13'
                if (i != 1):
                    url += '?pages=' + str(i)
                time.sleep(1)
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, "html.parser")
                spot_names = soup.find_all(class_="spot_name")
                for spot_name in spot_names:
                    links.append([
                        'https:' + spot_name.a.get("href"),
                        spot_name.a.string
                    ])
            self.write_matrix(links, self.base_path / file_name)
        else:
            print(
                '** error **',
                Path.cwd() / file_name,
                'has already existed'
            )

    def make_available_cars(self):
        if (not (Path.cwd() / 'stations_link.csv').exists()):
            print('** error ** there is no file about station links.')
        elif ((Path.cwd() / 'available_cars.csv').exists()):
            print('** error ** available_cars.csv has already existed')
        else:
            csv_file = open(
                self.base_path / 'stations_link.csv',
                'r',
                encoding='utf-8'
            )
            datas = list(csv.reader(csv_file, delimiter=","))
            avail_cars = []
            for i in tqdm(range(len(datas)), desc='scraiping...'):
                url = datas[i][0]
                time.sleep(1)
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, "html.parser")
                detail_contents = soup.find(class_="detail_contents")
                avail_car = detail_contents.find_all("dd")[2].string[:-1]
                avail_cars.append((datas[i][1], avail_car))
            self.write_matrix(
                avail_cars,
                self.base_path / 'available_cars.csv'
            )


if (__name__ == '__main__'):
    print('you have to import this file from another file')
