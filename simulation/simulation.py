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
        'SELECT_RATIO': 2,
        'CONFIG_NAME': 'default'
    }):
        if (params['NUMBER_OF_STATIONS'] * params['SELECT_RATIO'] > 1000):
            print('number of stations must be less than 1000')
            print('so we use 1000 as the NUMBER_OF_STATIONS.')
            params['NUMBER_OF_STATIONS'] = 1000 // params['SELECT_RATIO']
        self.NUMBER_OF_EMPLOYEES = params['NUMBER_OF_EMPLOYEES']
        self.TIME = params['TIME']
        self.C_IN = params['C_IN']
        self.C_OUT = params['C_OUT']
        self.C_E_FULL = params['C_E_FULL']
        self.PRICE_PER_15 = params['PRICE_PER_15']
        self.FUEL_CONSUMPTION = params['FUEL_CONSUMPTION']
        self.NUMBER_OF_STATIONS = params['NUMBER_OF_STATIONS']
        self.C_E_DAY = self.C_E_FULL * (self.TIME / 8 * 60)
        self.SELECT_RATIO = params['SELECT_RATIO']
        self.KIND_OF_AIP = {
            'spot_list': '/spot/list?',
            'category_list': '/category/list?',
            'route': '/route?'
        }
        self.base_path = PureWindowsPath(Path.cwd())
        self.sub_dir_path = self.base_path / params['CONFIG_NAME']
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

    def write_matrix(self, matrix, path, mode='x'):
        file = open(path, mode, encoding='utf-8')
        writer = csv.writer(file, lineterminator='\n')
        desc = 'making ' + path.name
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
        const_file_path = self.sub_dir_path / ('const.csv')
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
            params_spot['limit'] = str(self.NUMBER_OF_STATIONS * self.SELECT_RATIO)
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
            i = 1
            for spot in spots:
                if (i % self.SELECT_RATIO == 0):
                    S_coords.append([spot['coord']['lon'], spot['coord']['lat']])
                    S_codes.append(spot['code'].replace('-', '.'))
                i += 1
            self.write_matrix(
                S_coords,
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

    def get_station_traveltimes_and_distances(self):
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

        S_distances = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
        S_traveltimes = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
        for i in range(self.NUMBER_OF_STATIONS - 1):
            for j in range(i + 1, self.NUMBER_OF_STATIONS):
                time.sleep(1)
                if (self.S_coords[i] != self.S_coords[j]):
                    params_route['start'] = str(self.S_coords[i][1]) + ',' + str(self.S_coords[i][0])
                    params_route['goal'] = str(self.S_coords[j][1]) + ',' + str(self.S_coords[j][0])
                    time.sleep(0.65)
                    request = self.make_request(self.KIND_OF_AIP['route'], params_route)
                    response = self.get_response(request)
                    S_distances[i][j] = response['items'][0]['summary']['move']['distance']
                    S_distances[j][i] = response['items'][0]['summary']['move']['distance']
                    S_traveltimes[i][j] = response['items'][0]['summary']['move']['time']
                    S_traveltimes[j][i] = response['items'][0]['summary']['move']['time']
                else:
                    S_distances[i][j] = 0
                    S_traveltimes[i][j] = 0
        self.write_matrix(
            S_traveltimes,
            self.travel_file_path
        )
        self.write_matrix(
            S_distances,
            self.distance_file_path
        )

    def get_station_vhecles(self):
        S_vhecles = []
        for capa in self.S_capacities:
            S_vhecles.append(int(capa) - 1)
        self.write_matrix(
            S_vhecles,
            self.vhecle_file_path
        )

    def is_file_exist(self, file_path):
        return Path(file_path).exists()

    def get_all_datas(self):
        self.code_file_path = self.sub_dir_path / ('station_codes.csv')
        self.coord_file_path = self.sub_dir_path / ('station_coords.csv')
        self.url_file_path = self.sub_dir_path / ('station_urls.csv')
        self.capa_file_path = self.sub_dir_path / ('station_capacities.csv')
        self.travel_file_path = self.sub_dir_path / ('station_traveltimes.csv')
        self.distance_file_path = self.sub_dir_path / ('station_distances.csv')
        self.vhecle_file_path = self.sub_dir_path / ('station_vhecles.csv')

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
            self.S_capacities = list(map(int, self.S_capacities))
        else:
            self.get_station_capacities()
            self.get_all_datas()

        if (self.is_file_exist(self.travel_file_path) and self.is_file_exist(self.distance_file_path)):
            self.S_traveltimes = self.read_matrix(self.travel_file_path)
            self.S_traveltimes = np.array(self.S_traveltimes, dtype=int).tolist()
            self.S_distances = self.read_matrix(self.distance_file_path)
            self.S_distances = np.array(self.S_distances, dtype=int).tolist()
        else:
            self.get_station_traveltimes_and_distances()
            self.get_all_datas()

        if (self.is_file_exist(self.vhecle_file_path)):
            self.S_vhecles = self.read_matrix(self.vhecle_file_path)
            self.S_vhecles = list(map(int, self.S_vhecles))
        else:
            self.get_station_vhecles()
            self.get_all_datas()

    def excute(self):
        available_vhecles = np.zeros([self.NUMBER_OF_STATIONS, self.TIME + 1], dtype=int).tolist()
        for i in range(self.NUMBER_OF_STATIONS):
            for j in range(self.TIME + 1):
                available_vhecles[i][j] = self.S_vhecles[i]

        stations = list(range(self.NUMBER_OF_STATIONS))

        time_steps = list(range(self.TIME + 1))

        # demands = np.random.randint(-90, 2, (TIME - 1, NUMBER_OF_STATIONS, NUMBER_OF_STATIONS))
        demands = np.zeros([self.TIME, self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS], dtype=int).tolist()
        # test case 1
        demands[0][1][0] = 1
        demands[3][1][0] = 1

        price_per_L = 136.3
        distance_per_L = 35000
        price_per_distance = price_per_L / distance_per_L
        distance_per_min = 25000 / 60
        price_per_min = price_per_distance * distance_per_min

        rde = 0
        rdf = 0
        cost = 0
        success = 0
        time_over = 0

        result_file_path = self.sub_dir_path / 'result.csv'
        self.write_matrix(
            ['demands', 'rdf', 'rde', 'success', 'time_over'],
            result_file_path,
            mode='a'
        )

        for t in time_steps:
            if (t != self.TIME):
                for i in stations:
                    for j in stations:
                        if (i != j and demands[t][i][j]):
                            t_tmp = t + self.S_traveltimes[i][j]
                            if (t_tmp > self.TIME):
                                time_over += 1
                            else:
                                if (available_vhecles[i][t] == 0):
                                    rde += 1
                                if (available_vhecles[j][t_tmp] == self.S_capacities[j]):
                                    rdf += 1
                                if ((available_vhecles[i][t] != 0) and (available_vhecles[j][t_tmp] != self.S_capacities[j])):
                                    available_vhecles[i][t + 1:] = list(map(lambda x: x - 1, available_vhecles[i][t + 1:]))
                                    available_vhecles[j][t_tmp:] = list(map(lambda x: x + 1, available_vhecles[j][t_tmp:]))
                                    # cost += C[i][j]
                                    success += 1

            self.write_matrix(
                [np.array(demands).sum(), rdf, rde, success, time_over],
                result_file_path,
                mode='a'
            )
        self.write_matrix(
            available_vhecles,
            self.sub_dir_path / 'available_vhecles.csv'
        )
        for demand in demands:
            self.write_matrix(
                demand + [['-', '-', '-']],
                self.sub_dir_path / 'demands.csv',
                mode='a'
            )

    def test(self):
        print(np.array(demands).sum())


if (__name__ == '__main__'):
    print('you have to import this file from another file')
