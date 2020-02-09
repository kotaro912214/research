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
