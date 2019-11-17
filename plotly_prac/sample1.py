import plotly.graph_objects as go
import plotly
fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)
plotly.offline.plot(fig)
