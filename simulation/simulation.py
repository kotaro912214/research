from pathlib import Path, PureWindowsPath
import csv
import urllib.request
import urllib.parse
import json
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
import numpy as np

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
        file = open(path, 'x', encoding='utf-8')
        writer = csv.writer(file, lineterminator='\n')
        desc = 'making ' + path.name
        print(type(matrix[0]))
        # print(matrix)
        if (type(matrix[0]) == list or type(matrix[0]) == np.ndarray):
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
        const_file_path = self.sub_dir_path / ('const_' + str(self.NUMBER_OF_STATIONS) + '.csv')
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
            const_file_path
        )

    def get_station_codes_and_coords(self):
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
            self.S_coordss = []
            S_codes = []
            for spot in spots:
                self.S_coordss.append([spot['coord']['lon'], spot['coord']['lat']])
                # write_matrixが二次元配列に対してのみ対応するため，
                # 一つの値のみの要素でもリストにする必要がある．
                S_codes.append(spot['code'].replace('-', '.'))
            self.write_matrix(
                self.S_coordss,
                self.coord_file_path
            )
            self.write_matrix(
                S_codes,
                self.code_file_path
            )

    def get_station_urls(self):
        S_urls = []
        base_url = "https://navitime.co.jp/poi?spt="
        for i in tqdm(range(self.NUMBER_OF_STATIONS), desc='making urls...'):
            time.sleep(1)
            url = base_url + self.S_codes[i]
            S_urls.append(url)
        print(S_urls)
        self.write_matrix(
            S_urls,
            self.url_file_path
        )

    def get_station_capacities(self):
        S_capacities = []
        for i in tqdm(range(self.NUMBER_OF_STATIONS), desc='scraiping...'):
            url = self.S_urls[i]
            time.sleep(1)
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, "html.parser")
            detail_contents = soup.find(class_="detail_contents")
            avail_car = detail_contents.find_all("dd")[2].string[:-1]
            S_capacities.append(avail_car)
        self.write_matrix(
            S_capacities,
            self.capa_file_path
        )

    def get_station_traveltimes(self):
        params_route = {
            'car': '',
            'start': '',
            'goal': '',
            'order': '',
            'car-fuel': ''
        }
        params_route['car'] = 'only'
        params_route['order'] = 'total_distance'
        params_route['car-fuel'] = str(self.FUEL_CONSUMPTION)

        # Distance = np.zeros((NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
        S_traveltimes = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS))
        for i in range(self.NUMBER_OF_STATIONS - 1):
            for j in range(i + 1, self.NUMBER_OF_STATIONS):
                time.sleep(1)
                if (self.S_coords[i] != self.S_coords[j]):
                    params_route['start'] = str(self.S_coords[i][1]) + ',' + str(self.S_coords[i][0])
                    params_route['goal'] = str(self.S_coords[j][1]) + ',' + str(self.S_coords[j][0])
                    time.sleep(0.65)
                    request = self.make_request(self.KIND_OF_AIP['route'], params_route)
                    print(request)
                    response = self.get_response(request)
                    # Distance[i][j] = response['items'][0]['summary']['move']['distance']
                    # Distance[j][i] = response['items'][0]['summary']['move']['distance']
                    S_traveltimes[i][j] = response['items'][0]['summary']['move']['time']
                    S_traveltimes[j][i] = response['items'][0]['summary']['move']['time']
                else:
                    # Distance[i][j] = 0
                    S_traveltimes[i][j] = 0
        self.write_matrix(S_traveltimes, self.travel_file_path)

    def is_file_exist(self, file_path):
        return Path(file_path).exists()

    def get_all_datas(self):
        self.code_file_path = self.sub_dir_path / ('station_codes_' + str(self.NUMBER_OF_STATIONS) + '.csv')
        self.coord_file_path = self.sub_dir_path / ('station_coords_' + str(self.NUMBER_OF_STATIONS) + '.csv')
        self.url_file_path = self.sub_dir_path / ('station_urls_' + str(self.NUMBER_OF_STATIONS) + '.csv')
        self.capa_file_path = self.sub_dir_path / ('station_capacities_' + str(self.NUMBER_OF_STATIONS) + '.csv')
        self.travel_file_path = self.sub_dir_path / ('station_traveltimes_' + str(self.NUMBER_OF_STATIONS) + '.csv')

        if (self.is_file_exist(self.code_file_path) and self.is_file_exist(self.coord_file_path)):
            self.S_codes = self.read_matrix(self.code_file_path)
            self.S_coords = self.read_matrix(self.coord_file_path)
        else:
            self.get_station_codes_and_coords()
            self.get_all_datas()

        if (self.is_file_exist(self.url_file_path)):
            self.S_urls = self.read_matrix(self.url_file_path)
        else:
            self.get_station_urls()
            self.get_all_datas()

        if (self.is_file_exist(self.capa_file_path)):
            self.S_capacities = self.read_matrix(self.capa_file_path)
        else:
            self.get_station_capacities()
            self.get_all_datas()

        if (self.is_file_exist(self.travel_file_path)):
            self.S_traveltimes = self.read_matrix(self.travel_file_path)
        else:
            self.get_station_traveltimes()
            self.get_all_datas()

    def excute(self):
        print('a')


if (__name__ == '__main__'):
    print('you have to import this file from another file')
