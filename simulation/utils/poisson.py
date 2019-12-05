import plotly
import plotly.express as px
import numpy as np
import pandas as pd
NUM = 60 * 5
s_list = np.random.poisson(lam=0.07, size=(NUM + 1))
count = np.zeros((6, 2))
for i in range(len(count)):
    count[i][0] = i
for index, s in enumerate(s_list):
    count[s][1] += 1
df = pd.DataFrame(count, columns=['value', 'total of the value'])
fig = px.line(df, x='value', y='total of the value')
fig.update_traces(mode='markers+lines')
plotly.offline.plot(fig)
