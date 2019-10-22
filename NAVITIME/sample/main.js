const NUMBER_OF_STATIONS = 5;
const S_coords = get2dCsv('./datas/station_coords.csv');
let S_latlng = [];
for (var i = 0; i < NUMBER_OF_STATIONS; i++) {
  S_latlng[i] = new navitime.geo.LatLng(S_coords[i][0], S_coords[i][1]);
}
const baseUrl = 'https://api-challenge.navitime.biz/v1s/RLVVtSvxKmWi';
let renderer = null;
let S_traveltimes = [
  [0, 8, 9, 13, 11],
  [8, 0, 5, 9, 7],
  [9, 5, 0, 7, 7],
  [13, 9, 7, 0, 5],
  [11, 7, 7, 5, 0]
];

var t = 0;
const TIME = 20

function init() {
  center = new navitime.geo.LatLng('35.690171', '139.700378');
  map = new navitime.geo.Map('map', center, 1);
  fit();
  setPins();
  searchRoute();
  var id_timestep = setInterval(function() {
    updateFrame();
    if (t > TIME) {
      clearInterval(id_timestep);
    }
  }, 1000);
}

function fit() {
  var reDrawSettings = navitime.geo.Util.calcAutomaticAdjustmentViewPort(map, S_latlng);
  map.moveTo(reDrawSettings.latlng, reDrawSettings.zoom);
}

function setPins() {
  let pins = [];
  for (var i = 0; i < NUMBER_OF_STATIONS; i++) {
    pins[i] = new navitime.geo.overlay.Pin({
      icon: 'icons/pin-' + String(i) + '.png',
      position: S_latlng[i],
      draggable: false,
      map: map,
      title: 'station ' + String(i)
    });
  };
}

/**
 * エラーハンドラ
 * @param {Object} error
 */
function connectFailure(error) {
  alert(error);
}

function get2dCsv(url) {
  var txt = new XMLHttpRequest();
  txt.open('get', url, false);
  txt.send();
  var arr = txt.responseText.split('\n');
  var res = [];
  for (var i = 0; i < arr.length; i++) {
    if (arr[i] == '') break;
    res[i] = arr[i].split(',');
  }
  return res;
}

function searchRoute() {
  let start = S_coords[0];
  let goal = S_coords[2];
  const url = `${baseUrl}/route/shape?start=${start[0]},${start[1]}&goal=${goal[0]},${goal[1]}&add=transport_shape&car=only&shape-color=railway_line&datum=wgs84`;

  axios
    .get(url)
    .then(showRouteShape)
    .catch(connectFailure);
}

function showRouteShape(response) {
  if (renderer) {
    renderer.destroy();
  }

  const route = response.data;
  renderer = new navitime.geo.route.Renderer(route, {
    map: map,
    unit: 'degree',
    allRoute: false,
    arrow: true,
    originalColor: true,
  });
  renderer.draw();

}


var updateFrame = function() {
  for (var i = 0; i < NUMBER_OF_STATIONS - 1; i++) {
    for (var j = 0; j < NUMBER_OF_STATIONS - 1; j++) {
      if (vhecle_routes[t][i][j] != 0) {
        car[t][i][j][0] = new navitime.geo.overlay.Pin({
          icon: 'icons/car.png',
          position: new navitime.geo.LatLng(car[t][i][j][1][0], car[t][i][j][1][0]),
          draggable: false,
          map: map,
          title: 'customer'
        });
      }
    }
  }
  t++;
}

var moveCar = function(pin, ) {
  car_t[i][j]++;
  console.log(car_t[i][j]);
}

// const coords = [
//   String(Number(S_coords[i][0]) + t * 0.001),
//   S_coords[i][1]
// ];
// let pin = new navitime.geo.overlay.Pin({
//   icon: 'icons/car.png',
//   position: new navitime.geo.LatLng(coords[0], coords[1]),
//   draggable: false,
//   map: map,
//   title: 'customer'
// });