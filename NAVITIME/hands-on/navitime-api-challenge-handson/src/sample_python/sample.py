from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

BASE_URL = "https://api-challenge.navitime.biz/v1s/19999993"


@app.route('/')
def index():
    return render_template('index.html', title='NAVITIME API Sample')


@app.route('/spot')
def spot():
    return render_template('sample_spot.html', title='Spot Search Sample', value=None)


@app.route('/spot', methods=['POST'])
def get_spot():
    r = requests.get(BASE_URL + '/spot/list?word=%E6%9D%B1%E4%BA%AC%E3%82%BF%E3%83%AF%E3%83%BC&datum=wgs84')

    item = r.json()['items'][0]
    value = {
        'name': item['name'],
        'address': item['address_name'],
        'lat': item['coord']['lat'],
        'lon': item['coord']['lon']
    }

    return render_template('sample_spot.html', title='Spot Search Sample', value=value)


@app.route('/map')
def map():
    return render_template('sample_map.html', title='Map Sample')


if __name__ == '__main__':
    app.run(debug=True)
