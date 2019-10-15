function init() {
  // 都庁
  // 緯度・経度にdegree形式を利用する場合は必ず、シングルコーテーションで囲む
  // 通常はmillisec形式を推奨
  center = new navitime.geo.LatLng('35.690171', '139.700378')
  map = new navitime.geo.Map('map', center, 14)
}

const baseUrl = 'https://api-challenge.navitime.biz/v1s/RLVVtSvxKmWi';
let renderer = null;
let start = null;
let goal = null;

function search() {
  $('#loading').show();
  searchStartSpot();
}

function searchStartSpot() {
  const name = $('input[name=start]').val();
  const url = `${baseUrl}/spot/list?word=${name}&datum=wgs84`;

  // mochaリクエストをコンソールで確認
  console.log(url);

  axios
  // GETリクエスト
    .get(url)
    // 通信成功時に実行する関数
    .then(searchGoalSpot)
    // エラー発生時に実行する関数
    .catch(connectFailure);
}

function searchGoalSpot(response) {
  // APIレスポンスをコンソールで確認
  console.log(response);
  // 出発地点を設定
  start = response.data.items[0];

  // フォームから到着地点のキーワードを取得
  const name = $('input[name=goal]').val();
  // スポット検索リクエストURL
  const url = `${baseUrl}/spot/list?word=${name}&datum=wgs84`;

  axios
  // GETリクエスト
    .get(url)
    // 通信成功時に実行する関数
    .then(searchRoute)
    // エラー発生時に実行する関数
    .catch(connectFailure);
}

function searchRoute(response) {
  // APIレスポンスをコンソールで確認
  console.log(response);
  // 到着地点を設定
  goal = response.data.items[0];

  // ルート形式検索リクエストURL
  const url = `${baseUrl}/route/shape?start=${start.coord.lat},${start.coord.lon}&goal=${goal.coord.lat},${goal.coord.lon}&add=transport_shape&shape-color=railway_line&datum=wgs84`;

  axios
  // GETリクエスト
    .get(url)
    // 通信成功時に実行する関数
    .then(showRouteShape)
    // エラー発生時に実行する関数
    .catch(connectFailure);
}

function showRouteShape(response) {
  // APIレスポンスをコンソールで確認
  console.log(response);

  // 前回のルート線を削除
  if (renderer) {
    renderer.destroy();
  }

  // ルート線を地図上に描画
  const route = response.data;
  renderer = new navitime.geo.route.Renderer(route, {
    map: map,
    unit: 'degree',
    allRoute: true, // すべてのルートを表示するか
    arrow: true, // ルート線上に進行方向の矢印を表示するか
    originalColor: true, // 路線形状に指定された元々の色を利用するか
  });
  renderer.draw();

  // 検索終了
  $('#loading').hide();
}

/**
 * エラーハンドラ
 * @param {Object} error エラーオブジェクト
 */
function connectFailure(error) {
  alert(error);
}