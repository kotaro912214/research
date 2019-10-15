const NUMBER_OF_STATIONS = 5;
const S_coords = get2dCsv('station_coords.csv');
const S_latlng = [];
for (var i = 0; i < NUMBER_OF_STATIONS; i++) {
  S_latlng[i] = new navitime.geo.LatLng(S_coords[i][0], S_coords[i][1]);
}

function init() {
  center = new navitime.geo.LatLng('35.690171', '139.700378');
  map = new navitime.geo.Map('map', center, 1);
  setPins();
  fit();
}

function fit() {
  var reDrawSettings = navitime.geo.Util.calcAutomaticAdjustmentViewPort(map, S_latlng);
  map.moveTo(reDrawSettings.latlng, reDrawSettings.zoom);
}

function setPins() {
  const pins = [];
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

const baseUrl = 'https://api-challenge.navitime.biz/v1s/RLVVtSvxKmWi';
let renderer = null;

searchRoute();

function searchRoute(response) {
  let start = ['35.693308', '139.698652'];
  let goal = ['35.696695', '139.698528'];
  const url = `${baseUrl}/route/shape?start=${start[0]},${start[1]}&goal=${goal[0]},${goal[1]}&add=transport_shape&shape-color=railway_line&datum=wgs84`;

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