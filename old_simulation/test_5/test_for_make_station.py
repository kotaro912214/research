from pathlib import Path, PureWindowsPath
from bs4 import BeautifulSoup
import csv
from urllib import request
from tqdm import tqdm
import time

area_code = list(range(101, 124))
path = PureWindowsPath(Path.cwd()) / 'station_links.csv'

def get_station_links():
  for i in tqdm(range(1, 6)):
    if (i == 1):
      url = 'https://www.navitime.co.jp/category/0817001002/13'
    else:
      url = 'https://www.navitime.co.jp/category/0817001002/13/?page=' + str(i)
    time.sleep(1)
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    spot_names = soup.find_all(class_="spot_name")
    links = {}
    links[str(i)] = []
    for spot_name in tqdm(spot_names, desc='writing...'):
      links[str(i)].append((spot_name.a.get("href"), spot_name.a.string))
    print(links[str(i)])


get_station_links()
