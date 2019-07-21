from pathlib import Path, PureWindowsPath
import csv
import urllib.request, json
import urllib.parse
from tqdm import tqdm
from bs4 import BeautifulSoup
import time
from myfunc import my_round

# base_path = PureWindowsPath(Path.cwd())
# if ((Path.cwd() / 'station_links.csv').exists() and not (Path.cwd() / 'station_cars.csv').exists()):
#   csv_file = open(base_path / 'station_links.csv', 'r', encoding='utf-8')
#   datas = csv.reader(csv_file, delimiter=",")
#   avail_cars = []
#   for data in datas:
#     url = data[0]
#     time.sleep(1)
#     html = urllib.request.urlopen(url)
#     soup = BeautifulSoup(html, "html.parser")
#     avail_car = soup.find(class_="detail_contents").find_all("dd")[2].string
#     avail_cars.append((data[1], avail_car))
# else:
#   print('** error ** there is no file about station links.')
#   print("** error ** please excute 'Simulation.makeStationLinks()'")
a = tqdm(range(10))
for i in range(10):
  print(i)
  a.update()