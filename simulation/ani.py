import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

df = pd.read_csv('./v_coords_test/v_relational_coords.csv')
fig = px.scatter(
    df, x='x', y='y',
    animation_frame='t',
    range_x=[min(df['x']) - 10, max(df['x']) + 10],
    range_y=[min(df['y']) - 10, max(df['y']) + 10],
    color='type',
    size='size',
)

plotly.offline.plot(fig)
