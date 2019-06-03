import urllib.request, json
import urllib.parse
import datetime

api_path = './api.txt'
f = open(api_path)
API_KEY = f.read()


#Google Maps Platform Directions API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'

# origin = 'higashi omiya station'
origin = (35.949946, 139.645923)
destination = 'omiya station'
dep_time = '2019/07/31 09:55'

#UNIX時間の算出
dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
#dtime = dtime + datetime.timedelta(hours=9)
#print(dtime.timestamp())
unix_time = int(dtime.timestamp())

print('unixtime', unix_time)

nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(origin,destination,unix_time,API_KEY)
nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
request = endpoint + nav_request

#Google Maps Platform Directions APIを実行
response = urllib.request.urlopen(request).read()

#結果(JSON)を取得
directions = json.loads(response)

#所要時間を取得
for key in directions['routes']:
    #print(key) # titleのみ参照
    #print(key['legs']) 
    for key2 in key['legs']:
        print(key2['distance']['text'])
        print(key2['duration_in_traffic']['text'])
