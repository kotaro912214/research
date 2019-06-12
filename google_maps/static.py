import urllib.request, json
import urllib.parse
import datetime
import random
import numpy as np
import time

# create random coords for origins
def makeOrigin(n):
  origins = '&origins='
  for i in range(n):
    random_lat = round(random.uniform(35.641631, 35.784051), 6)
    random_lgn = round(random.uniform(139.570268, 139.739014), 6)
    origins += str(random_lat) + ',' + str(random_lgn)
    if (i != n - 1):
      origins += '|'
  return origins

# create random coords for destinations
def makeDestinations(n):
  destinations = '&destinations='
  for i in range(n):
    random_lat = round(random.uniform(35.641631, 35.784051), 6)
    random_lgn = round(random.uniform(139.570268, 139.739014), 6)
    destinations += str(random_lat) + ',' + str(random_lgn)
    if (i != n - 1):
      destinations += '|'
  return destinations


def main():
  # import API key from other file for perspective of security
  api_path = './api.txt'
  f = open(api_path)
  API_KEY = f.read()

  # count of data(origins and destinations)
  N = 10

  #create request from params
  endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
  key = '&key=' + API_KEY
  request = endpoint + makeOrigin(N) + makeDestinations(N) + key
  print(request)
  # send request and recieve response
  response = urllib.request.urlopen(request).read()
  directions = json.loads(response)

  # create matrix A which indicates shortest path between each origins and destinations
  A = np.zeros((N, N))
  i = 0
  j = 0
  # directions is a json object
  for row in directions['rows']:
    j = 0
    for element in row['elements']:
      distance = element['distance']['value']
      A[i][j] += distance
      j += 1
    i += 1

  print(A)

#-*- using:utf-8 -*-

if __name__ == '__main__':
  start = time.time()

  # write some processing codes here
  main()

  elapsed_time = time.time() - start
  print ("time:{0}".format(elapsed_time) + "[sec]")