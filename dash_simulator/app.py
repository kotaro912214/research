import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px
from simulation import Simulation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Relocation Simulator', style={'marginLeft': '30px'}),
    html.Div([
        html.Table([
            html.Tr([
                html.Th('time'),
                html.Th('number of stations'),
                html.Th('number of employees'),
                html.Th('station select ratio'),
                html.Th('config name')
            ]),
            html.Tr([
                html.Td(dcc.Input(id='input-time', placeholder='enter a time value', type='text', value='')),
                html.Td(dcc.Input(id='input-number-of-stations', placeholder='enter a number of stations', type='text', value='')),
                html.Td(dcc.Input(id='input-number-of-employees', placeholder='enter a number-of-employees', type='text', value='')),
                html.Td(dcc.Input(id='input-select-ratio', placeholder='enter a select ratio', type='text', value='')),
                html.Td(dcc.Input(id='input-config-name', placeholder='enter a config-name', type='text', value=''))
            ])
        ], style={'margin': 'auto', 'width': '95%'}),
        html.Table([
            html.Tr([
                html.Th('elastic vhecles'),
                html.Th('mu'),
                html.Th('sigma'),
                html.Th('significant digit'),
                html.Th('wt')
            ]),
            html.Tr([
                html.Td(dcc.Input(id='input-elastic-vhecles', placeholder='enter a elastic-vhecles', type='text', value='')),
                html.Td(dcc.Input(id='input-mu', placeholder='enter a mu', type='text', value='')),
                html.Td(dcc.Input(id='input-sigma', placeholder='enter a sigma', type='text', value='')),
                html.Td(dcc.Input(id='input-significant-digit', placeholder='enter a significant-digit', type='text', value='')),
                html.Td(dcc.Input(id='input-wt', placeholder='enter a wt', type='text', value=''))
            ])
        ], style={'margin': 'auto', 'width': '95%'}),
        html.Table([
            html.Tr([
                html.Th('make random demands'),
                html.Th('probability distribution mode'),
                html.Th('relocate'),
                html.Th('transition time'),
                html.Th('hub stations'),
                html.Th('lambda')
            ]),
            html.Tr([
                html.Td(dcc.RadioItems(id='input-make-random-demands', options=[{'label': 'True', 'value': 1}, {'label': 'False', 'value': 0}], value=1)),
                html.Td(dcc.Dropdown(id='input-random-mode', options=[{'label': 'poisson', 'value': 'poisson'}, {'label': 'normal', 'value': 'normal'}], value='poisson')),
                html.Td(dcc.RadioItems(id='input-relocate', options=[{'label': 'True', 'value': 1}, {'label': 'False', 'value': 0}], value=1)),
                html.Td(dcc.RadioItems(id='input-continuous-time', options=[{'label': 'True', 'value': 1}, {'label': 'False', 'value': 0}], value=1)),
                html.Td(dcc.Input(id='input-hub-stations', placeholder='enter a hub stations', type='text', value='')),
                html.Td(dcc.Input(id='input-lambda', placeholder='enter a lambda', type='text', value=''))
            ])
        ], style={'margin': 'auto', 'width': '95%'}),
    ], style={'marginBottom': '30px'}),
    html.Div([
        html.Button(id='auto-config-button', n_clicks=0, children='auto config', style={'marginRight': '30px'}),
        html.Button(id='submit_button', n_clicks=0, children='submit')
    ], style={'margin': 'auto', 'width': '30%'}),
    dcc.Graph(id='main_graph'),
    html.Div(id='tmp', style={'display': 'none'})
])

@app.callback(
    [
        Output('input-time', 'value'),
        Output('input-number-of-stations', 'value'),
        Output('input-number-of-employees', 'value'),
        Output('input-select-ratio', 'value'),
        Output('input-config-name', 'value'),
        Output('input-make-random-demands', 'value'),
        Output('input-random-mode', 'value'),
        Output('input-relocate', 'value'),
        Output('input-continuous-time', 'value'),
        Output('input-elastic-vhecles', 'value'),
        Output('input-mu', 'value'),
        Output('input-sigma', 'value'),
        Output('input-significant-digit', 'value'),
        Output('input-wt', 'value'),
        Output('input-hub-stations', 'value'),
        Output('input-lambda', 'value'),
    ],
    [Input('auto-config-button', 'n_clicks')]
)
def fill_with_auto_config(n_clicks):
    if (n_clicks > 0):
        return 30, 5, 1, 1, 'auto_config', 0, 'poisson', 1, 0, -1, -2.15, 1.27, 4, 0.1, 1, 0.03
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('tmp', 'children'),
    [Input('submit_button', 'n_clicks')],
    [
        State('input-time', 'value'),
        State('input-number-of-stations', 'value'),
        State('input-number-of-employees', 'value'),
        State('input-select-ratio', 'value'),
        State('input-config-name', 'value'),
        State('input-make-random-demands', 'value'),
        State('input-random-mode', 'value'),
        State('input-relocate', 'value'),
        State('input-continuous-time', 'value'),
        State('input-elastic-vhecles', 'value'),
        State('input-mu', 'value'),
        State('input-sigma', 'value'),
        State('input-significant-digit', 'value'),
        State('input-wt', 'value'),
        State('input-hub-stations', 'value'),
        State('input-lambda', 'value'),
    ]
)
def excute_simulation(
    n_clicks,
    time,
    number_of_stations,
    number_of_employees,
    select_ratio,
    config_name,
    make_random_demands,
    random_mode,
    relocate,
    continuous_time,
    elastic_vhecles,
    mu,
    sigma,
    significant_digit,
    wt,
    hub_stations,
    lambda_value
):
    if (n_clicks > 0):
        ins5 = Simulation(params={
            'TIME': int(time),
            'NUMBER_OF_STATIONS': int(number_of_stations),
            'NUMBER_OF_EMPLOYEES': int(number_of_employees),
            'SELECT_RATIO': int(select_ratio),
            'CONFIG_NAME': config_name,
            'MAKE_RANDOM_DEMANDS': bool(int(make_random_demands)),
            'RANDOM_MODE': random_mode,
            'RELOCATE': bool(int(relocate)),
            'CONTINUOUS_TIME': bool(int(continuous_time)),
            'ELASTIC_VHECLES': int(elastic_vhecles),
            'MU': float(mu),
            'SIGMA': float(sigma),
            'SIGNIFICANT_DIGIT': int(significant_digit),
            'W_T': float(wt),
            'HUB_STATIONS': [int(hub_stations)],
            'LAMBDA': float(lambda_value)
        })
        ins5.get_all_datas()
        ins5.excute()
        df = ins5.draw_vhecle_transitflow()
        return json.dumps(df.to_json())
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('main_graph', 'figure'),
    [Input('tmp', 'children')]
)
def update_main_graph(json_df):
    df = pd.read_json(json.loads(json_df))
    fig = create_main_figure(df)
    return fig

def create_main_figure(df):
    df = df.sort_values('index')
    return px.scatter(
        df, x='x', y='y',
        animation_frame='t',
        range_x=[min(df['x']) - 10, max(df['x']) + 10],
        range_y=[min(df['y']) - 10, max(df['y']) + 10],
        color='type',
        size='size',
    )


if __name__ == '__main__':
    app.run_server(debug=True)
