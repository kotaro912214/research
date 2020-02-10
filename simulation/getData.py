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


if (__name__ == "__main__"):
    print('use this file as a module')
