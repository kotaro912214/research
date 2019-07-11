import urllib.request, json
import urllib.parse

params_spot = {'category': '', 'coord': '', 'radius': '', 'limit': '', 'datum': ''}
params_spot['category'] = '0817001002' # category code of careco carsharing
params_spot['coord'] = '35.689296,139.702089' # a coord of shinjuku station
params_spot['radius'] = '100000'
params_spot['limit'] = '10'
params_spot['datum'] = 'tokyo'
url_params = urllib.parse.urlencode(params_spot)
request = 'https://api-challenge.navitime.biz/v1s/RLVVtSvxKmWi/spot/list?' + url_params
data = urllib.request.urlopen(request)