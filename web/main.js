function main() {
  setMapPosition(35.681236, 139.767125, 15);
  getPosition();
}

var num = 0;
var watch_id;

function clear() {
  navigator.geolocation.clearWatch(watch_id);
}

function setMapPosition(latitude, longitude, zoom) {
  var current_position = new google.maps.LatLng(latitude, longitude);
  var Options = {
    zoom: zoom, //地図の縮尺値
    center: current_position, //地図の中心座標
    mapTypeId: 'roadmap' //地図の種類
  };
  var map = new google.maps.Map(document.getElementById('map'), Options);
  var marker = new google.maps.Marker({ // マーカーの追加
    position: current_position, // マーカーを立てる位置を指定
    map: map // マーカーを立てる地図を指定
  });
}

function getPosition() {
  // navigator.geolocation.getCurrentPosition(test2, function(e) { alert(e.message); }, { "enableHighAccuracy": true, "timeout": 20000, "maximumAge": 2000 });
  watch_id = navigator.geolocation.watchPosition(displayTextPosition, function(e) { alert(e.message); }, { "enableHighAccuracy": true, "timeout": 20000, "maximumAge": 2000 });
}

function displayTextPosition(position) {

  var geo_text = "latitude:" + position.coords.latitude + "\n";
  geo_text += "longtitude:" + position.coords.longitude + "\n";
  geo_text += "accuracy:" + position.coords.accuracy + "\n";

  var date = new Date(position.timestamp);

  geo_text += "date:" + date.toLocaleString() + "\n";
  geo_text += "times:" + (++num) + "\n";

  document.getElementById('position_view').innerHTML = geo_text;

  setMapPosition(position.coords.latitude, position.coords.longitude, 15);

}

main()