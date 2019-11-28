import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv('./v_relational_coords.csv')
fig = px.scatter(
    df, x='x', y='y', animation_frame='t',
    range_x=[min(df['x']) - 10, max(df['x']) + 10],
    range_y=[min(df['y']) - 10, max(df['y']) + 10],
    color='type'
)

# px.scatter(df2, x='x', y='y', animation_frame='t', size='usage_stats')
plotly.offline.plot(fig)

# fig = go.Figure(
#     data=[go.Scatter(x=df1.x, y=df1.y)],
#     layout_title_text="a figure of transition flow"
# )
# plotly.offline.plot(fig)

# s = []
# for i in range(31):
#     s.append([39.84, 54.51, i, i])

# for i in range(31):
#     s.append([53.33, 53.94, i, i])

# for i in range(31):
#     s.append([60.16, 45.49, i, i])

# df = pd.DataFrame(s, columns=['y', 'x', 't', 'usage_stats'])
# df.to_csv('s_relational_coords.csv')
