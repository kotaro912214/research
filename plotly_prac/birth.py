import pandas as pd
import plotly

raw = pd.read_csv("./birth.csv")

data = [
    plotly.graph_objs.Bar(x=raw["year"], y=raw["births"], name="Births"),
    plotly.graph_objs.Scatter(x=raw["year"], y=raw["birth rate"], name="Birth Rate", yaxis="y2")
]
layout = plotly.graph_objs.Layout(
    title="Births and Birth Rate in Japan",
    legend={"x": 0.8, "y": 0.1},
    xaxis={"title": "Year", "range": [2000, 2016]},
    yaxis={"title": "Births", "rangemode": "tozero"},
    yaxis2={"title": "Birth Rate", "overlaying": "y", "side": "right"},
)
fig = plotly.graph_objs.Figure(data=data, layout=layout)
plotly.offline.plot(fig)
