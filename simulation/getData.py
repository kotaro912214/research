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


def read_sid(base_path):
    """SIDを読み込むためのメソッド．

    当たり前のことだが，コードはGitHub上で管理することになる．
    誤って流出してしまう場合を考慮してコード内に秘匿情報である，SIDを直接書くことはできない．
    したがってGitHub上では管理しないSID.txtというファイルにSIDを記述し，コードを実行する度にこれを動的に読み込む．

    Args:
        base_path: pathlib.PureWindowsPath, シミュレーションを実行するベースディレクトリのパスを示す．base_pathディレクトリ配下のSID.txtを参照する．

    Returns:
        str, 読み取ったSIDを返す．
    """
    sid_path = base_path / 'sid.txt'
    f = open(sid_path)
    SID = f.read()
    return SID


def make_request(base_path, api, params):
    """APIへのリクエストを作成するメソッド

    Args:
        base_path: pathlib.PureWindowsPath, シミュレーションを実行するベースディレクトリのパスを示す．
        aip: str, 利用するapiの種類を識別する文字列．
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
    request = base_url + read_sid(base_path) + api
    url_params = urllib.parse.urlencode(params)
    request += url_params
    return request


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


def is_exist(file_path):
    """ファイルが存在するかどうかを返すメソッド

    Args:
        file_path: pathlib.PureWindowsPath, 確認するファイルのパス．

    Returns:
        bool, 存在する場合はTrue, しない場合はFalseを返す．
    """
    return Path(file_path).exists()


if (__name__ == "__main__"):
    print('use this file as a module')
