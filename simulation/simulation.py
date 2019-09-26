from pathlib import Path, PureWindowsPath
import csv
import urllib.request
import urllib.parse
import json
import time

from tqdm import tqdm
from bs4 import BeautifulSoup

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
        'NUMBER_OF_STATIONS': 5,
        'CONFIG_NAME': 'default'
    }):
        if (params['NUMBER_OF_STATIONS'] > 1000):
            print('number of stations must be less than 1000')
            print('so we use 1000 as the NUMBER_OF_STATIONS.')
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
        self.CONFIG_NAME = params['CONFIG_NAME']
        self.base_path = PureWindowsPath(Path.cwd())
        self.sub_dir_path = self.base_path / self.CONFIG_NAME
        if (not Path(self.sub_dir_path).exists()):
            Path(self.sub_dir_path).mkdir()
            print("make sub directory")
        else:
            print(self.sub_dir_path.name, 'has already existed')
            print('we alternatively use the directory')

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
            if (type(matrix[0]) == list):
                writer.writerows(tqdm(matrix, desc=desc))
            else:
                writer.writerow(tqdm(matrix, desc=desc))
            file.close()

    def read_matrix(self, path):
        matrix = []
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                matrix.append(row)
            if (len(matrix) == 1):
                return matrix[0]
            else:
                return matrix

    def write_consts(self):
        file_name = 'const_' + str(self.NUMBER_OF_STATIONS) + '.csv'
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
            self.sub_dir_path / file_name
        )

    def get_station_codes_and_coords(self):
        coord_file_name = 'station_coords_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        code_file_name = 'station_codes_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        coord_file_exist = Path(self.sub_dir_path / coord_file_name).exists()
        code_file_exist = Path(self.sub_dir_path / code_file_name).exists()
        if ((not coord_file_exist) and (not code_file_exist)):
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
            S_coords = []
            S_codes = []
            for spot in spots:
                S_coords.append([spot['coord']['lon'], spot['coord']['lat']])
                # write_matrixが二次元配列に対してのみ対応するため，
                # 一つの値のみの要素でもリストにする必要がある．
                S_codes.append(spot['code'].replace('-', '.'))
            self.write_matrix(
                S_coords,
                self.sub_dir_path / coord_file_name
            )
            self.write_matrix(
                S_codes,
                self.sub_dir_path / code_file_name
            )
        else:
            print(
                '** error **',
                self.sub_dir_path / 'station_coords_?.csv or',
                self.sub_dir_path / 'station_codes_?.csv',
                'has already existed'
            )

    def get_station_urls(self):
        url_file_name = 'station_urls_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        url_file_exist = Path(self.sub_dir_path / url_file_name).exists()
        code_file_name = 'station_codes_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        code_file_exist = Path(self.sub_dir_path / code_file_name).exists()
        if ((not url_file_exist) and code_file_exist):
            S_codes = self.read_matrix(self.sub_dir_path / code_file_name)
            S_urls = []
            base_url = "https://navitime.co.jp/poi?spt="
            for i in tqdm(range(self.NUMBER_OF_STATIONS), desc='making urls...'):
                time.sleep(1)
                url = base_url + S_codes[i]
                S_urls.append(url)
            print(S_urls)
            self.write_matrix(
                S_urls,
                self.sub_dir_path / url_file_name
            )
        else:
            print(
                '** error **', self.sub_dir_path / url_file_name,
                'has already existed or',
                self.sub_dir_path / code_file_name, 'has not got yet'
            )

    def make_available_cars(self):
        link_file_name = 'stations_link_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        avail_file_name = 'available_cars_' + \
            str(self.NUMBER_OF_STATIONS) + '.csv'
        if (not (Path.cwd() / link_file_name).exists()):
            print('** error ** there is no file about station links.')
        elif ((Path.cwd() / avail_file_name).exists()):
            print('** error ** available_cars_?.csv has already existed')
        else:
            csv_file = open(
                self.base_path / link_file_name,
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
                self.base_path / avail_file_name
            )


if (__name__ == '__main__'):
    print('you have to import this file from another file')
