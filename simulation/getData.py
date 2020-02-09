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


def read_sid(base_path):
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
