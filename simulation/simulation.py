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

import getData


class Simulation():

    def __init__(self, params={
        'NUMBER_OF_EMPLOYEES': 5,
        'TIME': 60 * 8,
        'NUMBER_OF_STATIONS': 5,
        'SELECT_RATIO': 2,
        'CONFIG_NAME': 'default',
        'MAKE_RANDOM_DEMANDS': True,
        'RANDOM_MODE': 'poisson',
        'RELOCATE': True,
        'CONTINUOUS_TIME': True,
        'ELASTIC_VHECLES': -1,
        'MU': -2.15,
        'SIGMA': 1.27,
        'SIGNIFICANT_DIGIT': 3,
        'W_T': 0.1,
        'HUB_STATIONS': [],
        'LAMBDA': 0.05,
        'DEMANDD_PATH': 'demands.csv',
        'POPULATION': 10,
        'USER_RELOCATE': False,
        'EMPLOYEE_RELOCATE': False,
        'NEW_COST_FUNCTION': True
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
        self.KIND_OF_API = {
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
        self.moves = [['i', 'j', 't_start', 't_goal', 'current', 'mode']]
        self.W_T = params['W_T']
        self.HUB_STATIONS = params['HUB_STATIONS']
        self.LAMBDA = params['LAMBDA']
        self.RANDOM_MODE = params['RANDOM_MODE']
        self.DEMAND_PATH = params['DEMAND_PATH']
        self.POPULATION = params['POPULATION']
        self.USER_RELOCATE = params['USER_RELOCATE']
        self.EMPLOYEE_RELOCATE = params['EMPLOYEE_RELOCATE']
        self.NEW_COST_FUNCTION = params['NEW_COST_FUNCTION']
        self.users = Users(self.POPULATION, self.NUMBER_OF_STATIONS)
        if (not Path(self.sub_dir_path).exists()):
            Path(self.sub_dir_path).mkdir()
            print("make sub directory")
        else:
            # print(self.sub_dir_path.name, 'has already existed')
            # print('we alternatively use the directory')
            pass
        if (self.ELASTIC_VHECLES >= 0):
            Path(self.sub_dir_path / 'station_vhecles.csv').unlink()

    def get_all_datas(self):
        self.code_file_path = self.sub_dir_path / ('station_codes.csv')
        self.coord_file_path = self.sub_dir_path / ('station_coords.csv')
        self.url_file_path = self.sub_dir_path / ('station_urls.csv')
        self.capa_file_path = self.sub_dir_path / ('station_capacities.csv')
        self.travel_file_path = self.sub_dir_path / ('station_traveltimes.csv')
        self.distance_file_path = self.sub_dir_path / ('station_distances.csv')
        self.vhecle_file_path = self.sub_dir_path / ('station_vhecles.csv')

        if (getData.is_exist(self.code_file_path) and getData.is_exist(self.coord_file_path)):
            self.S_codes = getData.read_matrix(self.code_file_path)
            self.S_coords = getData.read_matrix(self.coord_file_path)
        else:
            getData.get_station_codes_and_coords(
                self.NUMBER_OF_STATIONS,
                self.SELECT_RATIO,
                self.sub_dir_path,
                self.KIND_OF_API
            )
            self.get_all_datas()

        if (getData.is_exist(self.url_file_path)):
            self.S_urls = getData.read_matrix(self.url_file_path)
        else:
            getData.get_station_urls(
                self.NUMBER_OF_STATIONS,
                self.S_codes,
                self.sub_dir_path
            )
            self.get_all_datas()

        if (getData.is_exist(self.capa_file_path)):
            self.S_capacities = getData.read_matrix(self.capa_file_path)
            self.S_capacities = list(map(int, self.S_capacities))
        else:
            getData.get_station_capacities(
                self.NUMBER_OF_STATIONS,
                self.S_urls,
                self.sub_dir_path
            )
            self.get_all_datas()

        if (getData.is_exist(self.travel_file_path) and getData.is_exist(self.distance_file_path)):
            self.S_traveltimes = getData.read_matrix(self.travel_file_path)
            self.S_traveltimes = np.array(
                self.S_traveltimes, dtype=int).tolist()
            self.S_distances = getData.read_matrix(self.distance_file_path)
            self.S_distances = np.array(self.S_distances, dtype=int).tolist()
            if ((self.CONTINUOUS_TIME and self.S_traveltimes[0][0] == 1) or (not self.CONTINUOUS_TIME and self.S_traveltimes[0][0] != 1)):
                Path(self.travel_file_path).unlink()
                Path(self.distance_file_path).unlink()
                getData.get_station_traveltimes_and_distances(
                    self.CONTINUOUS_TIME,
                    self.NUMBER_OF_STATIONS,
                    self.S_coords,
                    self.KIND_OF_API,
                    self.sub_dir_path
                )
                self.get_all_datas()
        else:
            getData.get_station_traveltimes_and_distances(
                self.CONTINUOUS_TIME,
                self.NUMBER_OF_STATIONS,
                self.S_coords,
                self.KIND_OF_API,
                self.sub_dir_path
            )
            self.get_all_datas()

        if (getData.is_exist(self.vhecle_file_path)):
            self.S_vhecles = getData.read_matrix(self.vhecle_file_path)
            self.S_vhecles = list(map(int, self.S_vhecles))
        else:
            getData.get_station_vhecles(self.S_capacities, self.sub_dir_path)
            self.get_all_datas()

    def read_demands(self):
        demads_file_path = self.base_path / self.DEMAND_PATH
        demands = getData.read_matrix(demads_file_path)
        new_demands = []
        for i in range((self.TIME + 1) * (self.NUMBER_OF_STATIONS + 1)):
            if ('-' not in demands[i][0]):
                new_demands.append(demands[i])
        threeD_demands = [None] * (self.TIME + 1)
        for t in range(self.TIME + 1):
            threeD_demands[t] = new_demands[t *
                                            self.NUMBER_OF_STATIONS:(t + 1) * self.NUMBER_OF_STATIONS]
        return np.array(threeD_demands, dtype=int).tolist()

    def make_available_vhecles(self):
        available_vhecles = np.zeros(
            [self.NUMBER_OF_STATIONS, self.TIME + 1], dtype=int).tolist()
        for i in range(self.NUMBER_OF_STATIONS):
            for j in range(self.TIME + 1):
                available_vhecles[i][j] = self.S_vhecles[i]
        return available_vhecles

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
        request = getData.make_request(
            self.base_path,
            self.KIND_OF_API['route_shape'],
            params_route_shape
        )
        response = getData.get_response(request)
        route_coords = []
        for path in response['items'][0]['path']:
            route_coords.append(path['coords'])
        return route_coords

    def make_vhecle_relational_coords(self):
        self.S_relational_coords = np.zeros((self.NUMBER_OF_STATIONS, 2))
        for i in range(self.NUMBER_OF_STATIONS):
            self.S_relational_coords[i][0] = self.coordinate_transformation(
                self.S_coords[i][0])
            self.S_relational_coords[i][1] = self.coordinate_transformation(
                self.S_coords[i][1])
        self.NUMBER_OF_VHECLES = sum(self.S_vhecles)
        self.V_relational_coords = np.zeros(
            (self.NUMBER_OF_VHECLES, self.TIME + 1, 2))
        i, j = 0, 0
        while (i < self.NUMBER_OF_VHECLES):
            self.V_relational_coords[i] = [
                [*self.S_relational_coords[j]]] * (self.TIME + 1)
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
            return getData.my_round(100 * (coord - self.x_lim[0]) / (self.x_lim[1] - self.x_lim[0]), self.SIGNIFICANT_DIGIT)
        else:
            return getData.my_round(100 * (coord - self.y_lim[0]) / (self.y_lim[1] - self.y_lim[0]), self.SIGNIFICANT_DIGIT)

    def update_vhecle_relational_coords(self, i, j, t_start, t_goal):
        dt = t_goal - t_start
        if (dt <= 0):
            print('**error** t_start and t_goal are same value')
        dx = getData.my_round(
            (self.S_relational_coords[j][1] - self.S_relational_coords[i][1]) / dt, self.SIGNIFICANT_DIGIT)
        dy = getData.my_round(
            (self.S_relational_coords[j][0] - self.S_relational_coords[i][0]) / dt, self.SIGNIFICANT_DIGIT)
        for v in range(self.NUMBER_OF_VHECLES):
            if (all(self.S_relational_coords[i] == self.V_relational_coords[v][t_start])):
                self.V_relational_coords[v][t_start][0] = getData.my_round(
                    self.V_relational_coords[v][t_start][0] + 0.0001, self.SIGNIFICANT_DIGIT)
                for t in range(t_start, t_goal - 1):
                    self.V_relational_coords[v][t + 1][1] = getData.my_round(
                        self.V_relational_coords[v][t][1] + dx, self.SIGNIFICANT_DIGIT)
                    self.V_relational_coords[v][t + 1][0] = getData.my_round(
                        self.V_relational_coords[v][t][0] + dy, self.SIGNIFICANT_DIGIT)
                self.V_relational_coords[v][t_goal:] = [
                    [*self.S_relational_coords[j]]] * len(self.V_relational_coords[v][t_goal:])
                return 1
        else:
            print('there is no vhecle that can be release.', i, j, t_start, t_goal)

    def draw_vhecle_transitflow(self):
        list_for_df1 = []
        for i in range(len(self.V_relational_coords)):
            for t in range(self.TIME + 1):
                list_for_df1.append(
                    ['car' + str(i), *self.V_relational_coords[i][t], t, 1])
        list_for_df2 = []
        for i in range(self.NUMBER_OF_STATIONS):
            for t in range(self.TIME + 1):
                if (i in self.HUB_STATIONS):
                    list_for_df2.append(
                        ['stations' + str(i), *self.S_relational_coords[i], t, 10])
                else:
                    list_for_df2.append(
                        ['stations' + str(i), *self.S_relational_coords[i], t, 5])
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
    def calculate_contract(
        self,
        available_vhecles,
        i,
        j,
        t_start,
        t_goal,
        demand
    ):
        rse = 0
        rsf = 0
        if (available_vhecles[i][t_start] >= demand):
            # all vhecles are available in i
            is_all_available = []
            for t in range(t_goal, self.TIME + 1):
                is_all_available.append(
                    available_vhecles[j][t] + demand <= self.S_capacities[j])
            if (all(is_all_available)):
                # parking is available
                can_contract = demand
            else:
                # parking is not available
                can_contract = self.S_capacities[j] - \
                    max(available_vhecles[j][t_goal:])
                rsf += (max(available_vhecles[j][t_goal:]
                            ) + demand - self.S_capacities[j])
        else:
            # all vhecles are not available in i
            is_all_available = []
            for t in range(t_goal, self.TIME + 1):
                is_all_available.append(
                    available_vhecles[j][t] + demand <= self.S_capacities[j])
            if (all(is_all_available)):
                # parking is available
                can_contract = available_vhecles[i][t_start]
                rse += (demand - available_vhecles[i][t_start])
            else:
                # parking is not available
                can_contract = min([
                    self.S_capacities[j] - max(available_vhecles[j][t_goal:]),
                    available_vhecles[i][t_start]
                ])
                rsf += (max(available_vhecles[j][t_goal:]
                            ) + demand - self.S_capacities[j])
                rse += (demand - available_vhecles[i][t_start])
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
        current,
        mode='demand'
    ):
        if (mode == 'user'):
            self.travel_distances['user'] += self.S_distances[i][j]
        elif (mode != 'demand'):
            self.travel_distances['jockey'] += self.S_distances[i][j]
        available_vhecles[i][t:] = list(
            map(lambda x: x - can_contract, available_vhecles[i][t:]))
        available_vhecles[j][t_tmp:] = list(
            map(lambda x: x + can_contract, available_vhecles[j][t_tmp:]))
        if (can_contract):
            self.moves.append([i, j, t, t_tmp, current, mode])
        # for _ in range(can_contract):
        #     self.update_vhecle_relational_coords(i, j, t, t_tmp)
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
                    # 上の条件式が真のとき下の条件式でエラーがでてしまうためこのコメントの上下のif文は一つにできない
                    if (available_vhecles[j][current + self.S_traveltimes[i][j]] == self.S_capacities[j]):
                        soonest_rsfs.append(
                            [j, current + self.S_traveltimes[i][j]])
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
                        # if (available_vhecles[i][t] > 0 and i != rse):これじゃだめ？
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
        make_rsf = 1 + \
            available_vhecles[goal][t_goal] - self.S_capacities[goal]
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
        make_rsf = 1 + \
            available_vhecles[goal][t_goal] - self.S_capacities[goal]
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
            cost = 1 / (E - G + 1) + delta + self.W_T * \
                self.S_traveltimes[start][goal]
        return cost

    def return_hub_vhecles(self, available_vhecles, demands, t):
        hub = self.HUB_STATIONS[0]
        for h in self.HUB_STATIONS:
            if (available_vhecles[h][t] < available_vhecles[hub][t]):
                hub = h
        if (t == self.TIME or available_vhecles[hub][t] >= self.S_capacities[hub] - 1):
            return available_vhecles
        can_release_list = [0] * self.NUMBER_OF_STATIONS
        for i in range(self.NUMBER_OF_STATIONS):
            if (i != hub):
                can_release_list[i] = available_vhecles[i][t]
                for j in range(self.NUMBER_OF_STATIONS):
                    can_release_list[i] -= demands[t][i][j]
        pool = can_release_list.index(max(can_release_list))
        if (t + self.S_traveltimes[pool][hub] > self.TIME):
            return available_vhecles
        if (pool > 0):
            can_contract, _, __ = self.calculate_contract(
                available_vhecles,
                pool,
                hub,
                t,
                t + self.S_traveltimes[pool][hub],
                1
            )
            available_vhecles = self.move_cars(
                available_vhecles,
                pool,
                hub,
                t,
                t + self.S_traveltimes[pool][hub],
                can_contract,
                t,
                'return_to_hub'
            )
        return available_vhecles

    def can_user_relocation(self, start):
        for i, location in enumerate(self.users.user_locations):
            if (location == start):
                p = np.random.rand()
                if (self.users.user_transitionfunc[i] <= p):
                    return True
        else:
            return False

    # @pysnooper.snoop('./log.log', prefix='excute ', max_variable_length=1500, watch=('available_vhecles'))
    def excute(self):
        available_vhecles = self.make_available_vhecles()
        available_vhecles_for_show = self.make_available_vhecles()
        if (self.MAKE_RANDOM_DEMANDS):
            demands = getData.make_demands(
                self.LAMBDA, self.TIME, self.NUMBER_OF_STATIONS)
        elif (getData.is_exist(self.base_path / self.DEMAND_PATH)):
            demands = self.read_demands()
        else:
            demands = getData.make_demands(
                self.LAMBDA, self.TIME, self.NUMBER_OF_STATIONS)
        # self.make_vhecle_relational_coords()
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
        self.travel_distances = {'user': 0, 'jockey': 0}
        result_file_path = self.sub_dir_path / 'result.csv'
        # getData.write_matrix(
        #     ['demands', 'rsf', 'rse', 'success', 'time_over', 'relocation_rsf_rse', 'relocation_rsf_avail', 'relocation_rse_release'],
        #     result_file_path,
        #     mode='a'
        # )

        for t in range(self.TIME + 1):
            i_j_list = []
            for i in range(self.NUMBER_OF_STATIONS):
                available_vhecles_for_show[i][t] = available_vhecles[i][t]
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
                    soonest_rsfs = self.look_for_soonest_rsf(
                        available_vhecles, t, demands)
                    for soonest_rsfs_item in soonest_rsfs:
                        soonest_rsf, rsf_target_time = soonest_rsfs_item
                        if (soonest_rsf >= 0):
                            soonest_rses = self.look_for_soonest_rse(
                                available_vhecles, t, rsf_target_time, demands, soonest_rsf)
                            for soonest_rses_item in soonest_rses:
                                soonest_rse, t_start = soonest_rses_item
                                if (soonest_rse >= 0):
                                    # relocation_rsf_rse += 1
                                    path_list.append([
                                        soonest_rsf,
                                        soonest_rse,
                                        t_start,
                                        t_start +
                                        self.S_traveltimes[soonest_rsf][soonest_rse],
                                        'rsf-rse'
                                    ])
                                else:
                                    avail_parks = self.look_for_available_park(
                                        available_vhecles, t, rsf_target_time, soonest_rsf)
                                    for avail_parks_item in avail_parks:
                                        available_park, available_time = avail_parks_item
                                        if (available_park >= 0):
                                            # relocation_rsf_avail += 1
                                            path_list.append([
                                                soonest_rsf,
                                                available_park,
                                                available_time,
                                                available_time +
                                                self.S_traveltimes[soonest_rsf][available_park],
                                                'rsf-avail'
                                            ])
                                        else:
                                            # update time
                                            pass
                        else:
                            soonest_rses = self.look_for_soonest_rse(
                                available_vhecles, t, rsf_target_time, demands, soonest_rsf)
                            for soonest_rses_item in soonest_rses:
                                soonest_rse, rse_target_time = soonest_rses_item
                                if (soonest_rse >= 0):
                                    release_parks = self.look_for_park_can_release(
                                        available_vhecles, t, rse_target_time, soonest_rse)
                                    for release_parks_item in release_parks:
                                        can_release, can_release_time = release_parks_item
                                        if (can_release >= 0):
                                            # relocation_rse_release += 1
                                            path_list.append([
                                                can_release,
                                                soonest_rse,
                                                can_release_time,
                                                can_release_time +
                                                self.S_traveltimes[can_release][soonest_rse],
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
                            if (self.NEW_COST_FUNCTION):
                                path_list[index].append(
                                    self.get_new_cost(
                                        available_vhecles,
                                        demands,
                                        *path
                                    )
                                )
                            else:
                                path_list[index].append(
                                    self.get_previous_cost(
                                        available_vhecles,
                                        demands,
                                        *path
                                    )
                                )
                        path_list = sorted(path_list, key=lambda x: x[5])
                        if (self.USER_RELOCATE and self.can_user_relocation(path_list[0][0])):
                            available_vhecles = self.move_cars(
                                available_vhecles, *path_list[0][:4], 1, t, 'user')
                        elif (self.EMPLOYEE_RELOCATE):
                            available_vhecles = self.move_cars(
                                available_vhecles, *path_list[0][:4], 1, t, path_list[0][4])

            if (len(self.HUB_STATIONS)):
                available_vhecles = self.return_hub_vhecles(
                    available_vhecles,
                    demands,
                    t
                )

            for i_j in i_j_list:
                i = i_j[0]
                j = i_j[1]
                if (i != j and demands[t][i][j]):
                    t_tmp = t + self.S_traveltimes[i][j]
                    if (t_tmp > self.TIME):
                        time_over += 1
                    else:
                        can_contract, rsf_tmp, rse_tmp = self.calculate_contract(
                            available_vhecles,
                            i,
                            j,
                            t,
                            t_tmp,
                            demands[t][i][j]
                        )
                        rsf += rsf_tmp
                        rse += rse_tmp
                        available_vhecles = self.move_cars(
                            available_vhecles, i, j, t, t_tmp, can_contract, t)
                        success += can_contract

            if (t == self.TIME):
                getData.write_matrix(
                    [self.LAMBDA, np.array(demands).sum(), rsf, rse, success, time_over,
                     relocation_rsf_rse, relocation_rsf_avail, relocation_rse_release],
                    result_file_path,
                    mode='a'
                )
            rsf_list.append(rsf)
            rse_list.append(rse)
            success_list.append(success)
        if (getData.is_exist(self.sub_dir_path / ('available_vhecles.csv'))):
            Path(self.sub_dir_path / ('available_vhecles.csv')).unlink()
        available_vhecles_for_show = np.insert(
            available_vhecles_for_show, 0, np.arange(self.TIME + 1), axis=0)
        # getData.write_matrix(
        #     available_vhecles_for_show,
        #     self.sub_dir_path / 'available_vhecles.csv'
        # )
        # new_result = [
        #     ['item'] + np.arange(self.TIME + 1).tolist(),
        #     ['rsf'] + rsf_list,
        #     ['rse'] + rse_list,
        #     ['success'] + success_list
        # ]
        # getData.write_matrix(
        #     new_result,
        #     self.sub_dir_path / 'new_result.csv',
        #     mode='a'
        # )
        getData.write_matrix(
            [x for x in self.travel_distances.values()],
            self.sub_dir_path / 'traevl_distances.csv',
            mode='a'
        )
        # getData.write_matrix(
        #     self.users.user_locations,
        #     self.sub_dir_path / 'user_locations.csv',
        #     mode='w'
        # )
        # if (len(self.moves)):
        #     getData.write_matrix(
        #         self.moves,
        #         self.sub_dir_path / 'moves.csv',
        #         mode='a'
        #     )
        # if (self.MAKE_RANDOM_DEMANDS):
        #     for index, demand in enumerate(demands):
        #         getData.write_matrix(
        #             demand,
        #             self.sub_dir_path / 'demands.csv',
        #             mode='a'
        #         )
        #         line = '-' * (self.NUMBER_OF_STATIONS * 2)
        #         line = str(index) + line[1:]
        #         getData.write_matrix(
        #             [line],
        #             self.sub_dir_path / 'demands.csv',
        #             mode='a'
        #         )


class Users():

    def __init__(self, population, number_of_stations):
        self.POPULATION = population
        self.NUMBER_OF_STATIONS = number_of_stations
        self.user_locations = np.random.randint(
            self.NUMBER_OF_STATIONS, size=self.POPULATION)
        self.user_transitionfunc = np.random.rand(self.POPULATION)
        self.user_transitionfunc_estimated = np.zeros((self.POPULATION))


if (__name__ == '__main__'):
    print('you have to use this class by importing this from another file')
