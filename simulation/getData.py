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


def my_round(val, digit=0):
    """値を四捨五入するメソッド．

    組み込み関数のroundメソッドだと誤差が生じる．
    任意の有効桁数で四捨五入するメソッドを定義．

    Args:
        val: float, 四捨五入する値
        digit: int, 有効桁数，デフォルトでは0．

    Returns:
        四捨五入した値を返す．
        digitが0の場合int，0でない場合はfloatで返す．
    """
    p = 10 ** digit
    if (digit == 0):
        return int((val * p * 2 + 1) // 2 / p)
    else:
        return (val * p * 2 + 1) // 2 / p


def read_sid():
    """SIDを読み込むためのメソッド．

    当たり前のことだが，コードはGitHub上で管理することになる．
    誤って流出してしまう場合を考慮してコード内に秘匿情報である，SIDを直接書くことはできない．
    したがってGitHub上では管理しないSID.txtというファイルにSIDを記述し，コードを実行する度にこれを動的に読み込む．

    Args:
        None

    Returns:
        str, 読み取ったSIDを返す．
    """
    sid_path = PureWindowsPath(Path.cwd()) / 'sid.txt'
    f = open(sid_path)
    SID = f.read()
    return SID


def make_request(api, params):
    """APIへのリクエストを作成するメソッド

    Args:
        api: str, 利用するapiの種類を識別する文字列．
            example:

            '/spot/list?'

        params: dict, URLで利用するパラメータとその値を格納した辞書．
            example:

            {
                'category': '0817001002',
                'coord': '35.689296,139.702089',
                'radius': '100',
                'limit': '10',
                'datum': 'tokyo'
            }

    Returns:
        str, 作成したAPIリクエストを実行するためのURLを返す．
        example:

        'https://api-challenge.navitime.biz/v1s/sid/spot/list?category=0817001002&coord={35.689296,139.702089}&radius=100&limit=10&datum=tokyo'

    """
    base_url = 'https://api-challenge.navitime.biz/v1s/'
    request = base_url + read_sid() + api
    url_params = urllib.parse.urlencode(params)
    request += url_params
    return request


def get_response(request):
    """APIのリクエストを投げてレスポンスを返すメソッド

    Args:
        request: str, make_requestで作成したリクエストURL
        example:

        'https://api-challenge.navitime.biz/v1s/sid/spot/list?category=0817001002&coord={35.689296,139.702089}&radius=100&limit=10&datum=tokyo'

    Returns:
        dict, 結果のJSON形式文字列をPython辞書形式で返します．
        example:

        {'items': [{'coord': {'lat': 52.37839, 'lng': 139.479484}}, ]}
    """
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


def read_matrix(path):
    """csvファイルを配列として読み込むメソッド

    Args:
        path: pathlib.PureWindowsPath, 読み込むファイルのパス．

    Returns:
        list, 読み込むファイルが一行の場合一次元配列を，複数行の場合二次元配列を返す．
    """
    matrix = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            matrix.append(row)
        if (len(matrix) == 1):
            return matrix[0]
        else:
            return matrix


def write_matrix(matrix, path, mode='x'):
    """任意の行列を任意のファイルに書き込むメソッド

    単なる組み込み関数の処理のみでも実装可能だが，一次元と二次元の配列を処理する必要があるためそれを判断してファイル書き込みを行う．

    Args:
        matrix: list, np.ndarray, 任意の配列．Python組み込みのlsit型とnumpyの多次元配列どちらにも対応している．
        path: str, pathlib.PureWindowsPath, 書き込むファイルのパス．文字列の相対パス，PureWindowsPathのどちらにも対応している．
        mode: str, ファイルの書き込みモードを文字列で指定．'a', 'x'のどちらか．

    Returns:
        None
    """
    file = open(path, mode, encoding='utf-8')
    writer = csv.writer(file, lineterminator='\n')
    desc = 'making ' + path.name
    if (type(matrix[0]) == list or type(matrix[0]) == np.ndarray):
        writer.writerows(tqdm(matrix, desc=desc))
    else:
        writer.writerow(tqdm(matrix, desc=desc))
    file.close()


def is_exist(file_path):
    """ファイルが存在するかどうかを返すメソッド

    Args:
        file_path: pathlib.PureWindowsPath, 確認するファイルのパス．

    Returns:
        bool, 存在する場合はTrue, しない場合はFalseを返す．
    """
    return Path(file_path).exists()


def get_station_codes_and_coords(N, SELECT_RATIO, sub_dir_path, KIND_OF_API):
    """ステーションの識別コードと座標を取得するメソッド

    Args:
        N: int, 読み込むステーション数を示す整数．
        SELECT_RATIO: int, ステーションの選択比率を示す整数．
        sub_dir_path: PureWindowsPath, str, 取得した情報をCSV形式で出力するファイルの相対パス．

    Returns:
        None
    """
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
    params_spot['limit'] = str(N * SELECT_RATIO)
    params_spot['datum'] = 'tokyo'
    # get the data of the station list
    request = make_request(
        KIND_OF_API['spot_list'],
        params_spot
    )
    response = get_response(request)
    spots = response['items']
    S_coords = []
    S_codes = []
    i = 1
    for spot in spots:
        if (i % SELECT_RATIO == 0):
            S_coords.append([spot['coord']['lat'], spot['coord']['lon']])
            S_codes.append(spot['code'].replace('-', '.'))
        i += 1
    write_matrix(
        S_coords,
        sub_dir_path / 'station_coords.csv'
    )
    write_matrix(
        S_codes,
        sub_dir_path / 'station_codes.csv'
    )


def get_station_traveltimes_and_distances(CONSIDER_TRAVEL_TIME, N, S_coords, KIND_OF_API, sub_dir_path):
    """ステーションの移動時間と距離を同時に取得するメソッド

    Args:
        CONSIDER_TRAVEL_TIME: bool, 移動時間を考慮するかどうかを示すブール値
        N: int, 読み込むステーション数を示す整数．
        S_coords: list, ステーションの座標が格納されている配列
        KIND_OF_API: dict, 利用するAPIの種類とその識別値を格納する辞書
        sub_dir_path: PureWindowsPath, str, 取得した情報をCSV形式で出力するファイルの相対パス．

    Returns:
        None
    """
    if (CONSIDER_TRAVEL_TIME):
        params_route = {
            'car': 'only',
            'start': '',
            'goal': '',
            'order': 'total_distance',
        }
        S_distances = np.zeros(
            (N, N), dtype=int).tolist()
        S_traveltimes = np.zeros(
            (N, N), dtype=int).tolist()
        for i in range(N - 1):
            for j in tqdm(
                range(i + 1, N),
                desc='searching route of ' + str(i) + '...'
            ):
                if (S_coords[i] != S_coords[j]):
                    params_route['start'] = str(
                        S_coords[i][0]) + ',' + str(S_coords[i][1])
                    params_route['goal'] = str(
                        S_coords[j][0]) + ',' + str(S_coords[j][1])
                    request = make_request(
                        KIND_OF_API['route'],
                        params_route
                    )
                    response = get_response(request)
                    S_distances[i][j] = response['items'][0]['summary']['move']['distance']
                    S_distances[j][i] = response['items'][0]['summary']['move']['distance']
                    S_traveltimes[i][j] = response['items'][0]['summary']['move']['time']
                    S_traveltimes[j][i] = response['items'][0]['summary']['move']['time']
                else:
                    S_distances[i][j] = 0
                    S_traveltimes[i][j] = 0
        write_matrix(
            S_traveltimes,
            sub_dir_path / 'station_traveltimes.csv'
        )
        write_matrix(
            S_distances,
            sub_dir_path / 'station_distances.csv'
        )
    else:
        S_distances = np.zeros((N, N), dtype=int).tolist()
        S_traveltimes = np.ones((N, N), dtype=int).tolist()
        write_matrix(
            S_traveltimes,
            sub_dir_path / 'station_traveltimes.csv'
        )
        write_matrix(
            S_distances,
            sub_dir_path / 'station_distances.csv'
        )


def get_station_urls(N, S_codes, sub_dir_path):
    """ステーション情報の取得に必要なステーションごとの詳細サイトURLを取得するメソッド

    Args:
        N: int, 読み込むステーション数を示す整数.
        S_codes: list, ステーションを識別するコードが格納されている配列
        sub_dir_path: PureWindowsPath, str, 取得したURLをCSV形式で出力するファイルの相対パス．

    Returns:
        None
    """
    S_urls = []
    base_url = "https://navitime.co.jp/poi?spt="
    for i in tqdm(range(N), desc='making urls...'):
        url = base_url + S_codes[i]
        S_urls.append(url)
    write_matrix(
        S_urls,
        sub_dir_path / 'station_urls.csv'
    )


def get_station_capacities(N, S_urls, sub_dir_path):
    """スクレイピングによってステーションの駐車可能台数を取得するメソッド

    Args:
        N: int, 読み込むステーション数を示す整数.
        S_urls: list, 各ステーションの詳細サイトのURLが格納されている配列．
        sub_dir_path: PureWindowsPath, str, 取得したURLをCSV形式で出力するファイルの相対パス．

    Returns:
        None
    """
    S_capacities = []
    for i in tqdm(range(N), desc='scraiping...'):
        url = S_urls[i]
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        detail_contents = soup.find(class_="detail_contents")
        avail_car = detail_contents.find_all("dd")[2].string[:-1]
        S_capacities.append(int(avail_car) + 1)
    write_matrix(
        S_capacities,
        sub_dir_path / 'station_capacities.csv'
    )


def get_station_vhecles(S_capacities, sub_dir_path):
    S_vhecles = []
    for capa in S_capacities:
        S_vhecles.append(int(capa) - 1)
    write_matrix(
        S_vhecles,
        sub_dir_path / 'station_vhecles.csv'
    )


def make_demands(LAMBDA, T, N):
    demands = np.random.poisson(lam=LAMBDA, size=(
        T + 1, N, N))
    for t in range(T + 1):
        for i in range(N):
            for j in range(N):
                if (any([
                    demands[t][i][j] <= 0,
                    i == j,
                    t == T,
                ])):
                    demands[t][i][j] = 0
    return demands


if (__name__ == "__main__"):
    print('use this file as a module')
