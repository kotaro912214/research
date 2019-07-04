# coding: UTF-8

import urllib.request, json
import urllib.parse
import datetime
import random
import numpy as np
import time


def readSID():
  sid_path = './sid.txt'
  f = open(sid_path)
  SID = f.read()
  return SID

what_api = {'spot_list':'/spot/list?', 'category_list': '/category/list?'}

def main():
  base_url = 'https://api-challenge.navitime.biz/v1s/' + readSID()
  request = base_url + what_api['spot_list']
  # 0817001002 カレコのカテゴリコード
  request += 'category=0817001002'
  # word = urllib.parse.quote('港区')
  # request += '&word=' + word
  request += '&coord=35.689296,139.702089'
  request += '&radius=1800'
  request += '&limit=100'
  request += '&datum=wgs84'
  print(request)
  response = urllib.request.urlopen(request).read()
  json_res = json.loads(response)
  spots = json_res['items']
  # NUMBER_OF_STATIONS = json_res['count']
  S_coord = []
  for spot in spots:
    S_coord.append((spot['coord']['lon'], spot['coord']['lat']))


if (__name__ == '__main__'):
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print('実行時間: ', elapsed_time)