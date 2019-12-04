from pathlib import Path
from pathlib import PureWindowsPath
import csv
import urllib.request
import urllib.parse
import json
import time
import pprint

from tqdm import tqdm
from bs4 import BeautifulSoup
import numpy as np
import pysnooper
import matplotlib
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import pandas as pd

from myfunc import my_round

class Simulation():

    def __init__(self, params={
        'NUMBER_OF_EMPLOYEES': 5,
        'TIME': 60 * 8,
        'NUMBER_OF_STATIONS': 5,
        'SELECT_RATIO': 2,
        'CONFIG_NAME': 'default',
        'MAKE_RANDOM_DEMANDS': True,
        'RELOCATE': True,
        'CONTINUOUS_TIME': True,
        'ELASTIC_VHECLES': -1,
        'MU': -2.15,
        'SIGMA': 1.27,
        'SIGNIFICANT_DIGIT': 3,
        'W_T': 0.1
    }):
        if (params['NUMBER_OF_STATIONS'] * params['SELECT_RATIO'] > 1000):
            print('number of stations must be less than 1000')
            print('so we use 1000 as the NUMBER_OF_STATIONS.')
            params['NUMBER_OF_STATIONS'] = 1000 // params['SELECT_RATIO']
        self.NUMBER_OF_EMPLOYEES = params['NUMBER_OF_EMPLOYEES']
        self.TIME = params['TIME']
        self.NUMBER_OF_STATIONS = params['NUMBER_OF_STATIONS']
        self.SELECT_RATIO = params['SELECT_RATIO']
        self.MAKE_RANDOM_DEMANDS = params['MAKE_RANDOM_DEMANDS']
        self.RELOCATE = params['RELOCATE']
        self.CONFIG_NAME = params['CONFIG_NAME']
        self.CONTINUOUS_TIME = params['CONTINUOUS_TIME']
        self.ELASTIC_VHECLES = params['ELASTIC_VHECLES']
        self.MU = params['MU']
        self.SIGMA = params['SIGMA']
        self.KIND_OF_AIP = {
            'spot_list': '/spot/list?',
            'category_list': '/category/list?',
            'route': '/route?',
            'route_shape': '/route/shape?'
        }
        self.SIGNIFICANT_DIGIT = params['SIGNIFICANT_DIGIT']
        self.base_path = PureWindowsPath(Path.cwd())
        self.sub_dir_path = self.base_path / self.CONFIG_NAME
        self.x_lim = []
        self.y_lim = []
        self.moves = []
        self.W_T = params['W_T']
        if (not Path(self.sub_dir_path).exists()):
            Path(self.sub_dir_path).mkdir()
            print("make sub directory")
        else:
            print(self.sub_dir_path.name, 'has already existed')
            print('we alternatively use the directory')
        if (self.ELASTIC_VHECLES >= 0):
            Path(self.sub_dir_path / 'station_vhecles.csv').unlink()

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
                S_coords.append([spot['coord']['lat'], spot['coord']['lon']])
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
            S_capacities.append(int(avail_car) + 1)
        self.write_matrix(
            S_capacities,
            self.capa_file_path
        )

    def get_station_traveltimes_and_distances(self):
        if (self.CONTINUOUS_TIME):
            params_route = {
                'car': 'only',
                'start': '',
                'goal': '',
                'order': 'total_distance',
            }
            S_distances = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
            S_traveltimes = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
            for i in range(self.NUMBER_OF_STATIONS - 1):
                for j in tqdm(
                    range(i + 1, self.NUMBER_OF_STATIONS),
                    desc='searching route of ' + str(i) + '...'
                ):
                    time.sleep(1)
                    if (self.S_coords[i] != self.S_coords[j]):
                        params_route['start'] = str(self.S_coords[i][0]) + ',' + str(self.S_coords[i][1])
                        params_route['goal'] = str(self.S_coords[j][0]) + ',' + str(self.S_coords[j][1])
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
        else:
            S_distances = np.zeros((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
            S_traveltimes = np.ones((self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS), dtype=int).tolist()
            self.write_matrix(
                S_traveltimes,
                self.travel_file_path
            )
            self.write_matrix(
                S_distances,
                self.distance_file_path
            )

    def get_station_vhecles(self):
        self.S_vhecles = []
        for capa in self.S_capacities:
            if (self.ELASTIC_VHECLES >= 0):
                self.S_vhecles.append(self.ELASTIC_VHECLES)
            else:
                self.S_vhecles.append(int(capa) - 1)
        self.write_matrix(
            self.S_vhecles,
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
            if ((self.CONTINUOUS_TIME and self.S_traveltimes[0][0] == 1) or (not self.CONTINUOUS_TIME and self.S_traveltimes[0][0] != 1)):
                Path(self.travel_file_path).unlink()
                Path(self.distance_file_path).unlink()
                self.get_station_traveltimes_and_distances()
                self.get_all_datas()
        else:
            self.get_station_traveltimes_and_distances()
            self.get_all_datas()

        if (self.is_file_exist(self.vhecle_file_path)):
            self.S_vhecles = self.read_matrix(self.vhecle_file_path)
            self.S_vhecles = list(map(int, self.S_vhecles))
        else:
            self.get_station_vhecles()
            self.get_all_datas()

    def make_random_demands(self):
        # demands = np.random.normal(loc=-2.15, scale=1.27, size=(self.TIME + 1, self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS))
        demands = np.random.normal(loc=self.MU, scale=self.SIGMA, size=(self.TIME + 1, self.NUMBER_OF_STATIONS, self.NUMBER_OF_STATIONS))
        demands = np.round(demands).astype('int')
        for t in range(self.TIME + 1):
            for i in range(self.NUMBER_OF_STATIONS):
                for j in range(self.NUMBER_OF_STATIONS):
                    if (demands[t][i][j] <= 0 or i == j or t == self.TIME):
                        demands[t][i][j] = 0
        return demands

    def read_demands(self):
        demads_file_path = self.sub_dir_path / 'demands.csv'
        demands = self.read_matrix(demads_file_path)
        new_demands = []
        for i in range((self.TIME + 1) * (self.NUMBER_OF_STATIONS + 1)):
            if (demands[i] != ['-' * (self.NUMBER_OF_STATIONS * 2)]):
                new_demands.append(demands[i])
        threeD_demands = [None] * (self.TIME + 1)
        for t in range(self.TIME + 1):
            threeD_demands[t] = new_demands[t * self.NUMBER_OF_STATIONS:(t + 1) * self.NUMBER_OF_STATIONS]
        return np.array(threeD_demands, dtype=int).tolist()

    def make_available_vhecles(self):
        available_vhecles = np.zeros([self.NUMBER_OF_STATIONS, self.TIME + 1], dtype=int).tolist()
        for i in range(self.NUMBER_OF_STATIONS):
            for j in range(self.TIME + 1):
                available_vhecles[i][j] = self.S_vhecles[i]
        return available_vhecles

    def draw_rsf_graph(self):
        matplotlib.use('Agg')
        rsf_list = self.read_matrix(self.sub_dir_path / 'rsf.csv')
        rsf_list = np.array(rsf_list).astype('int')
        t = np.linspace(0, self.TIME, self.TIME + 1)
        plt.plot(t, rsf_list[0], color="red", label='non relocation')
        plt.plot(t, rsf_list[1], color="blue", label='relocation')
        plt.legend()
        plt.grid()
        plt.title('only rsf considered')
        plt.xlim(0, self.TIME + 1)
        plt.ylim(0, np.amax(rsf_list) * 1.1)
        plt.xlabel('time')
        plt.ylabel('a number of rsf')
        plt.savefig(self.sub_dir_path / 'rsf.png')
        plt.clf()

    def draw_rse_graph(self):
        matplotlib.use('Agg')
        rse_list = self.read_matrix(self.sub_dir_path / 'rse.csv')
        rse_list = np.array(rse_list).astype('int')
        plt.plot(np.linspace(0, self.TIME, self.TIME + 1), rse_list[0], color="red", label='non relocation')
        plt.plot(np.linspace(0, self.TIME, self.TIME + 1), rse_list[1], color="blue", label='relocation')
        plt.legend()
        plt.grid()
        plt.title('only rse considered')
        plt.xlim(0, self.TIME + 1)
        plt.ylim(0, max(max(rse_list[0]), max(rse_list[1])) * 1.1)
        plt.xlabel('time')
        plt.ylabel('a number of rse')
        plt.savefig(self.sub_dir_path / 'rse.png')
        plt.clf()

    def make_route_coords(self, start, goal):
        params_route_shape = {
            'car': 'only',
            'start': '',
            'goal': '',
            'format': 'json',
            'add': 'transport_shape',
            'shape-color': 'railway_line',
            'datum': 'wgs84'
        }
        # params_route_shape['start'] = '35.706822,139.813956'
        # params_route_shape['goal'] = '35.706822,139.815956'
        params_route_shape['start'] = start
        params_route_shape['goal'] = goal
        request = self.make_request(self.KIND_OF_AIP['route_shape'], params_route_shape)
        response = self.get_response(request)
        route_coords = []
        for path in response['items'][0]['path']:
            route_coords.append(path['coords'])
        return route_coords

    def make_vhecle_relational_coords(self):
        self.S_relational_coords = np.zeros((self.NUMBER_OF_STATIONS, 2))
        for i in range(self.NUMBER_OF_STATIONS):
            self.S_relational_coords[i][0] = self.coordinate_transformation(self.S_coords[i][0])
            self.S_relational_coords[i][1] = self.coordinate_transformation(self.S_coords[i][1])
        self.NUMBER_OF_VHECLES = sum(self.S_vhecles)
        self.V_relational_coords = np.zeros((self.NUMBER_OF_VHECLES, self.TIME + 1, 2))
        i, j = 0, 0
        while (i < self.NUMBER_OF_VHECLES):
            self.V_relational_coords[i] = [[*self.S_relational_coords[j]]] * (self.TIME + 1)
            i += 1
            if (i >= sum(self.S_vhecles[:j + 1])):
                j += 1

    def coordinate_transformation(self, coord):
        coord = float(coord)
        if (self.x_lim == []):
            x_lim = [999.000, 0.000]
            y_lim = [999.000, 0.000]
            for i in range(self.NUMBER_OF_STATIONS):
                y_lim[0] = min(y_lim[0], float(self.S_coords[i][0]))
                x_lim[0] = min(x_lim[0], float(self.S_coords[i][1]))
                y_lim[1] = max(y_lim[1], float(self.S_coords[i][0]))
                x_lim[1] = max(x_lim[1], float(self.S_coords[i][1]))
            self.x_lim = [x_lim[0] - 0.01, x_lim[1] + 0.01]
            self.y_lim = [y_lim[0] - 0.01, y_lim[1] + 0.01]
        if (coord > 100.0):
            return my_round(100 * (coord - self.x_lim[0]) / (self.x_lim[1] - self.x_lim[0]), self.SIGNIFICANT_DIGIT)
        else:
            return my_round(100 * (coord - self.y_lim[0]) / (self.y_lim[1] - self.y_lim[0]), self.SIGNIFICANT_DIGIT)

    def update_vhecle_relational_coords(self, i, j, t_start, t_goal):
        dt = t_goal - t_start
        if (dt <= 0):
            print('**error** t_start and t_goal are same value')
        dx = my_round((self.S_relational_coords[j][1] - self.S_relational_coords[i][1]) / dt, self.SIGNIFICANT_DIGIT)
        dy = my_round((self.S_relational_coords[j][0] - self.S_relational_coords[i][0]) / dt, self.SIGNIFICANT_DIGIT)
        for v in range(self.NUMBER_OF_VHECLES):
            if (all(self.S_relational_coords[i] == self.V_relational_coords[v][t_start])):
                self.V_relational_coords[v][t_start][0] = my_round(self.V_relational_coords[v][t_start][0] + 0.0001, self.SIGNIFICANT_DIGIT)
                for t in range(t_start, t_goal - 1):
                    self.V_relational_coords[v][t + 1][1] = my_round(self.V_relational_coords[v][t][1] + dx, self.SIGNIFICANT_DIGIT)
                    self.V_relational_coords[v][t + 1][0] = my_round(self.V_relational_coords[v][t][0] + dy, self.SIGNIFICANT_DIGIT)
                self.V_relational_coords[v][t_goal:] = [[*self.S_relational_coords[j]]] * len(self.V_relational_coords[v][t_goal:])
                return 1
        else:
            print('there is no vhecle that can be release.', i, j, t_start, t_goal)

    def make_station_usage_stats(self):
        self.S_usage_stats = np.zeros((self.NUMBER_OF_STATIONS, self.TIME + 1))
        for i in range(self.NUMBER_OF_STATIONS):
            self.S_usage_stats[i][0] = my_round(self.S_vhecles[i] / self.S_capacities[i], 2)

    def draw_vhecle_transitflow(self):
        list_for_df1 = []
        for i in range(len(self.V_relational_coords)):
            t = 0
            for col in self.V_relational_coords[i]:
                list_for_df1.append(['car' + str(i), *col, t, 1])
                t += 1
        list_for_df2 = []
        for i in range(self.NUMBER_OF_STATIONS):
            t = 0
            for col in self.S_usage_stats[i]:
                list_for_df2.append(['stations' + str(i), *self.S_relational_coords[i], t, 5])
                t += 1
        columns = ['type', 'y', 'x', 't', 'size']
        list_for_df = list_for_df1 + list_for_df2
        df = pd.DataFrame(data=list_for_df, columns=columns)
        df.to_csv(self.sub_dir_path / 'v_relational_coords.csv')
        fig = px.scatter(
            df, x='x', y='y',
            animation_frame='t',
            range_x=[min(df['x']) - 10, max(df['x']) + 10],
            range_y=[min(df['y']) - 10, max(df['y']) + 10],
            color='type',
            size='size',
        )
        plotly.offline.plot(fig)

    # @pysnooper.snoop('./log.log', prefix='calc_contract ', max_variable_length=500)
    def caluculate_contract(
        self,
        available_vhecles_start,
        available_vhecles_target,
        capacity_target,
        demand,
        t
    ):
        rse = 0
        rsf = 0
        if (available_vhecles_start >= demand):
            # all vhecles are available in i
            if (available_vhecles_target + demand <= capacity_target):
                # parking is available
                can_contract = demand
            else:
                # parking is not available
                can_contract = capacity_target - available_vhecles_target
                rsf += (available_vhecles_target + demand - capacity_target)
        else:
            # all vhecles are not available in i
            if (available_vhecles_target + demand <= capacity_target):
                # parking is available
                can_contract = available_vhecles_start
                rse += (demand - available_vhecles_start)
            else:
                # parking is not available
                can_contract = min([
                    capacity_target - available_vhecles_target,
                    available_vhecles_start
                ])
                rsf += (available_vhecles_target + demand - capacity_target)
                rse += (demand - available_vhecles_start)
        return [can_contract, rsf, rse]

    # @pysnooper.snoop('./log.log', prefix='move_cars ', max_variable_length=1000)
    def move_cars(
        self,
        available_vhecles,
        i,
        j,
        t,
        t_tmp,
        can_contract,
        current
    ):
        available_vhecles[i][t:] = list(map(lambda x: x - can_contract, available_vhecles[i][t:]))
        available_vhecles[j][t_tmp:] = list(map(lambda x: x + can_contract, available_vhecles[j][t_tmp:]))
        self.moves.append([i, j, t, t_tmp, current])
        for _ in range(can_contract):
            self.update_vhecle_relational_coords(i, j, t, t_tmp)
        return available_vhecles

    # @pysnooper.snoop('./log.log', prefix='rsf ', max_variable_length=1000)
    def look_for_soonest_rsf(self, available_vhecles, current, demands):
        soonest_rsfs = []
        for i in range(self.NUMBER_OF_STATIONS):
            for j in range(self.NUMBER_OF_STATIONS):
                if (all([
                    demands[current][i][j],
                    current + self.S_traveltimes[i][j] <= self.TIME,
                ])):
                    if (available_vhecles[j][current + self.S_traveltimes[i][j]] == self.S_capacities[j]):
                        soonest_rsfs.append([j, current + self.S_traveltimes[i][j]])
        if (len(soonest_rsfs)):
            return soonest_rsfs
        else:
            return [[-1, current]]

    # @pysnooper.snoop('./log.log', prefix='rse ', max_variable_length=1000)
    def look_for_soonest_rse(self, available_vhecles, current, rsf_target_time, demands, rsf):
        soonest_rses = []
        if (rsf >= 0):
            for t_start in range(current, rsf_target_time + 1):
                for i in range(self.NUMBER_OF_STATIONS):
                    for t_end in range(t_start + self.S_traveltimes[rsf][i], self.TIME - self.S_traveltimes[rsf][i]):
                        for j in range(self.NUMBER_OF_STATIONS):
                            if (all([
                                demands[t_end][i][j],
                                i != rsf,
                                available_vhecles[i][t_end] < demands[t_end][i][j],
                                available_vhecles[rsf][t_start] > 0
                            ])):
                                soonest_rses.append([i, t_start])
                                break
                        else:
                            continue
                        break
            if (len(soonest_rses)):
                return soonest_rses
            else:
                return [[-1, current]]
        else:
            for t in range(current, self.TIME):
                for i in range(self.NUMBER_OF_STATIONS):
                    for j in range(self.NUMBER_OF_STATIONS):
                        if (demands[t][i][j] and available_vhecles[i][t] == 0):
                            soonest_rses.append([i, t])
            else:
                if (len(soonest_rses)):
                    return soonest_rses
                else:
                    return [[-1, current]]

    # @pysnooper.snoop('./log.log', prefix='available_park ', max_variable_length=1000)
    def look_for_available_park(self, available_vhecles, current, rsf_ratget_time, rsf):
        avail_parks = []
        for t in range(current, rsf_ratget_time + 1):
            for i in range(self.NUMBER_OF_STATIONS):
                if (t + self.S_traveltimes[rsf][i] <= self.TIME and rsf != i):
                    if (available_vhecles[i][t + self.S_traveltimes[rsf][i]] < self.S_capacities[i] and available_vhecles[rsf][t] > 0):
                        avail_parks.append([i, t])
        if (len(avail_parks)):
            return avail_parks
        else:
            return [[-1, current]]

    # @pysnooper.snoop('./log.log', prefix='can_release ', max_variable_length=1000)
    def look_for_park_can_release(self, available_vhecles, current, rse_target_time, rse):
        release_parks = []
        for t in range(current, rse_target_time):
            for i in range(self.NUMBER_OF_STATIONS):
                if (t + self.S_traveltimes[i][rse] <= rse_target_time):
                    if (available_vhecles[i][t] > 0):
                        release_parks.append([i, t])
        if (len(release_parks)):
            return release_parks
        else:
            return [[-1, current]]

    def get_previous_cost(self, available_vhecles, demands, start, goal, t_start, t_goal, mode):
        E_table = {
            'rsf-rse': [2, t_start + 1],
            'rsf-avail': [1, t_start + 1],
            'rse-release': [1, t_goal]
        }
        E = E_table[mode][0]
        t_e = E_table[mode][1]
        G = 0
        t_g = 100
        make_rse = 1 - available_vhecles[start][t_start + 1]
        for j in range(self.NUMBER_OF_STATIONS):
            if (demands[t_start + 1][start][j]):
                make_rse += demands[t_start + 1][start][j]
                t_g = min([t_g, t_start + 1])
        if (make_rse > 0):
            G += make_rse
        make_rsf = 1 + available_vhecles[goal][t_goal] - self.S_capacities[goal]
        for i in range(self.NUMBER_OF_STATIONS):
            for t in range(t_start, t_goal - self.S_traveltimes[i][goal] + 1):
                if (demands[t][i][goal]):
                    make_rsf += demands[t][i][goal]
                    t_g = min([t_g, t])
        if (make_rsf > 0):
            G += make_rsf
        delta = (G / (t_g + 1)) - (E / (t_e + 1))
        if (E - G + 1 <= 0):
            cost = 100
        else:
            cost = 1 / (E - G + 1) + delta
        return cost

    def get_new_cost(self, available_vhecles, demands, start, goal, t_start, t_goal, mode):
        E_table = {
            'rsf-rse': [2, t_start + 1],
            'rsf-avail': [1, t_start + 1],
            'rse-release': [1, t_goal]
        }
        E = E_table[mode][0]
        t_e = E_table[mode][1]
        G = 0
        t_g = 100
        make_rse = 1 - available_vhecles[start][t_start + 1]
        for j in range(self.NUMBER_OF_STATIONS):
            if (demands[t_start + 1][start][j]):
                make_rse += demands[t_start + 1][start][j]
                t_g = min([t_g, t_start + 1])
        if (make_rse > 0):
            G += make_rse
        make_rsf = 1 + available_vhecles[goal][t_goal] - self.S_capacities[goal]
        for i in range(self.NUMBER_OF_STATIONS):
            for t in range(t_start, t_goal - self.S_traveltimes[i][goal] + 1):
                if (demands[t][i][goal]):
                    make_rsf += demands[t][i][goal]
                    t_g = min([t_g, t])
        if (make_rsf > 0):
            G += make_rsf
        delta = (G / (t_g + 1)) - (E / (t_e + 1))
        if (E - G + 1 <= 0):
            cost = 100
        else:
            cost = 1 / (E - G + 1) + delta + self.W_T * self.S_traveltimes[start][goal]
        return cost

    # @pysnooper.snoop('./log.log', prefix='excute ', max_variable_length=1500, watch=('available_vhecles'))
    def excute(self):
        available_vhecles = self.make_available_vhecles()
        available_vhecles_for_show = self.make_available_vhecles()
        if (self.MAKE_RANDOM_DEMANDS):
            demands = self.make_random_demands()
        elif (self.is_file_exist(self.sub_dir_path / 'demands.csv')):
            demands = self.read_demands()
        else:
            demands = self.make_random_demands()
        self.make_vhecle_relational_coords()
        self.make_station_usage_stats()
        rse = 0
        rsf = 0
        success = 0
        time_over = 0
        relocation_rsf_avail = 0
        relocation_rsf_rse = 0
        relocation_rse_release = 0
        rsf_list = []
        rse_list = []
        success_list = []
        result_file_path = self.sub_dir_path / 'result.csv'
        self.write_matrix(
            ['demands', 'rsf', 'rse', 'success', 'time_over', 'relocation_rsf_rse', 'relocation_rsf_avail', 'relocation_rse_release'],
            result_file_path,
            mode='a'
        )

        for t in range(self.TIME + 1):
            i_j_list = []
            for i in range(self.NUMBER_OF_STATIONS):
                available_vhecles_for_show[i][t] = available_vhecles[i][t]
                self.S_usage_stats[i][t] = my_round(available_vhecles[i][t] / self.S_capacities[i], 2)
                for j in range(self.NUMBER_OF_STATIONS):
                    if (i == j):
                        continue
                    i_j_list.append((
                        i, j,
                        self.S_capacities[i] - available_vhecles[i][t],
                        sum([row[j] for row in demands[t]]),
                    ))
            i_j_list = sorted(i_j_list, key=lambda x: (x[2], x[3]))

            # relocation
            if (self.RELOCATE):
                for e in range(self.NUMBER_OF_EMPLOYEES):
                    path_list = []
                    soonest_rsfs = self.look_for_soonest_rsf(available_vhecles, t, demands)
                    for soonest_rsfs_item in soonest_rsfs:
                        soonest_rsf, rsf_target_time = soonest_rsfs_item
                        if (soonest_rsf >= 0):
                            soonest_rses = self.look_for_soonest_rse(available_vhecles, t, rsf_target_time, demands, soonest_rsf)
                            for soonest_rses_item in soonest_rses:
                                soonest_rse, t_start = soonest_rses_item
                                if (soonest_rse >= 0):
                                    # relocation_rsf_rse += 1
                                    path_list.append([
                                        soonest_rsf,
                                        soonest_rse,
                                        t_start,
                                        t + self.S_traveltimes[soonest_rsf][soonest_rse],
                                        'rsf-rse'
                                    ])
                                else:
                                    avail_parks = self.look_for_available_park(available_vhecles, t, rsf_target_time, soonest_rsf)
                                    for avail_parks_item in avail_parks:
                                        available_park, available_time = avail_parks_item
                                        if (available_park >= 0):
                                            # relocation_rsf_avail += 1
                                            path_list.append([
                                                soonest_rsf,
                                                available_park,
                                                available_time,
                                                available_time + self.S_traveltimes[soonest_rsf][available_park],
                                                'rsf-avail'
                                            ])
                                        else:
                                            # update time
                                            pass
                        else:
                            soonest_rses = self.look_for_soonest_rse(available_vhecles, t, rsf_target_time, demands, soonest_rsf)
                            for soonest_rses_item in soonest_rses:
                                soonest_rse, rse_target_time = soonest_rses_item
                                if (soonest_rse >= 0):
                                    release_parks = self.look_for_park_can_release(available_vhecles, t, rse_target_time, soonest_rse)
                                    for release_parks_item in release_parks:
                                        can_release, can_release_time = release_parks_item
                                        if (can_release >= 0):
                                            # relocation_rse_release += 1
                                            path_list.append([
                                                can_release,
                                                soonest_rse,
                                                can_release_time,
                                                t + self.S_traveltimes[can_release][soonest_rse],
                                                'rse-release'
                                            ])
                                        else:
                                            # update time
                                            pass
                                else:
                                    # no more feasible path
                                    pass
                    if (len(path_list)):
                        for index, path in enumerate(path_list):
                            path_list[index].append(
                                self.get_previous_cost(
                                    available_vhecles,
                                    demands,
                                    *path
                                )
                            )
                        sorted(path_list, key=lambda x: x[5])
                        available_vhecles = self.move_cars(available_vhecles, *path_list[0][:4], 1, t)

            for i_j in i_j_list:
                i = i_j[0]
                j = i_j[1]
                if (i != j and demands[t][i][j]):
                    t_tmp = t + self.S_traveltimes[i][j]
                    if (t_tmp > self.TIME):
                        time_over += 1
                    else:
                        if (available_vhecles[i][t] == 0):
                            rse += demands[t][i][j]
                        if (available_vhecles[j][t_tmp] == self.S_capacities[j]):
                            rsf += demands[t][i][j]
                        if ((available_vhecles[i][t] != 0) and (available_vhecles[j][t_tmp] != self.S_capacities[j])):
                            can_contract, rsf_tmp, rse_tmp = self.caluculate_contract(
                                available_vhecles[i][t],
                                available_vhecles[j][t_tmp],
                                self.S_capacities[j],
                                demands[t][i][j],
                                t
                            )
                            rsf += rsf_tmp
                            rse += rse_tmp
                            available_vhecles = self.move_cars(available_vhecles, i, j, t, t_tmp, can_contract, t)
                            success += can_contract

            self.write_matrix(
                [np.array(demands).sum(), rsf, rse, success, time_over, relocation_rsf_rse, relocation_rsf_avail, relocation_rse_release],
                result_file_path,
                mode='a'
            )
            rsf_list.append(rsf)
            rse_list.append(rse)
            success_list.append(success)
        if (self.is_file_exist(self.sub_dir_path / ('available_vhecles.csv'))):
            Path(self.sub_dir_path / ('available_vhecles.csv')).unlink()
        self.write_matrix(
            available_vhecles_for_show,
            self.sub_dir_path / 'available_vhecles.csv'
        )
        self.write_matrix(
            rsf_list,
            self.sub_dir_path / 'rsf.csv',
            mode='a'
        )
        self.write_matrix(
            rse_list,
            self.sub_dir_path / 'rse.csv',
            mode='a'
        )
        self.write_matrix(
            success_list,
            self.sub_dir_path / 'success.csv',
            mode='a'
        )
        if (len(self.moves)):
            self.write_matrix(
                self.moves,
                self.sub_dir_path / 'moves.csv',
                mode='a'
            )
        if (self.MAKE_RANDOM_DEMANDS):
            for demand in demands:
                self.write_matrix(
                    demand,
                    self.sub_dir_path / 'demands.csv',
                    mode='a'
                )
                self.write_matrix(
                    ['-' * (self.NUMBER_OF_STATIONS * 2)],
                    self.sub_dir_path / 'demands.csv',
                    mode='a'
                )


if (__name__ == '__main__'):
    print('you have to use this class by importing this from another file')
