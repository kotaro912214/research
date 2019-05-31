# モジュールのインポート
import pandas as pd
import urllib
import urllib.error
import urllib.request

# Google API モジュール
from pygeocoder import Geocoder
import googlemaps

API_KEY = 'AIzaSyB1hzdNcmuujGGhI8N0SLLC7u_QI8ib7YY'
output_path = './'
pixel = '640x480'
scale = '18'

# geocodeで取得できる情報の一覧の例（国会議事堂の場合）
gmaps = googlemaps.Client(key=API_KEY)
address = u'国会議事堂'
result = gmaps.geocode(address)
result


