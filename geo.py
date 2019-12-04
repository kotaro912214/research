import plotly.express as px
px.set_mapbox_access_token(open(".mapbox_token").read())
carshare = px.data.carshare()
fig = px.scatter_mapbox(
    carshare,
    lat="centroid_lat",
    lon="centroid_lon",
    color="peak_hour",
    size="car_hours",
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=10
)
fig.show()
