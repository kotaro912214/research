import plotly
import plotly.express as px
# gap = px.data.gapminder()
# print(gap)
election = px.data.election()
fig = px.scatter_3d(
    election,
    x="Joly",
    y="Coderre",
    z="Bergeron",
    color="winner",
    size="total",
    hover_name="district",
    symbol="result",
    color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"}
)
# plotly.offline.plot(fig)
