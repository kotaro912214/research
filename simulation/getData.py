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
        val: float. 四捨五入する値
        digit: int. 有効桁数，デフォルトでは0．

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
        base_path: str. シミュレーションを実行するベースディレクトリのパスを示す．base_pathディレクトリ配下のSID.txtを参照する．

    Returns:
        str. 読み取ったSIDを返す．
    """
    sid_path = base_path / 'sid.txt'
    f = open(sid_path)
    SID = f.read()
    return SID


def make_request(base_path, api, params):
    base_url = 'https://api-challenge.navitime.biz/v1s/'
    request = base_url + read_sid(base_path) + api
    url_params = urllib.parse.urlencode(params)
    request += url_params
    return request


def read_matrix(path):
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
    return Path(file_path).exists()