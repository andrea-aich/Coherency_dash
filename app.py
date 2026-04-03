import dash
from dash import html, dcc
# from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True, date_format='%Y-%m-%d')
df.index = pd.to_datetime(df['Date'])

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='twelve columns div-Create-your-sources',
                    children=[
                        html.H2('Create your sources.'),
                        html.P('They are like the ingredients of your cake that you will later mix together.'),
                        html.P('Use the sliders to change the frequency of the sources.'),
                        html.Div(className='source A', children=[
                            html.Div(className='three columns div-slider-A',
                                 children=[
                                    html.P('Frequency A'),
                                    dcc.Slider(id='freq-slider-A', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='eight columns div-sources-plot-A',
                                 children=[
                                     dcc.Graph(id='source-A',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                        html.Div(className='source B', children=[
                            html.Div(className='three columns div-slider-B',
                                 children=[
                                    html.P('Frequency B'),
                                    dcc.Slider(id='freq-slider-B', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='eight columns div-sources-plot-B',
                                 children=[
                                     dcc.Graph(id='source-B',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                        html.Div(className='source C', children=[
                            html.Div(className='three columns div-slider-C',
                                 children=[
                                    html.P('Frequency C'),
                                    dcc.Slider(id='freq-slider-C', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='eight columns div-sources-plot-C',
                                 children=[
                                     dcc.Graph(id='source-C',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                    ]
                ),
        html.Div(className='twelve columns div-Compute-coherency',
                    children=[
                        html.H2('Compute coherency'),
                        html.P('Use the sliders to choose the frequency and time window.')
                    ]
                ),        
        html.Div(className='rows',
                 children=[
                    html.Div(className='eight columns div-user-controls',
                             children=[
                                 html.H2('DASH - STOCK PRICES'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                                                      multi=True, value=[df['stock'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='four columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries',
                                     config={'displayModeBar': False},
                                     animate=True),
                                 dcc.Graph(id='change',
                                     config={'displayModeBar': False},
                                     animate=True),
                             ])
                             
                              ])
    ])


# Callback for timeseries price
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure


@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['change'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Daily Change', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure



# trying my own callback for the sliders
@app.callback(Output('source-A', 'figure'),
                [Input('freq-slider-A', 'value')])   
def update_sources_plot(freq_a):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 10, 500)
    source_a = np.sin(freq_a * x)
    trace_a = go.Scatter(x=x, y=source_a, mode='lines', name='Source A')
    
    figure = {'data': [trace_a],
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Sources', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }

    return figure


@app.callback(Output('source-B', 'figure'),
                [Input('freq-slider-B', 'value')])   
def update_sources_plot(freq_b):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 10, 500)
    source_b = np.sin(freq_b * x)
    trace_b = go.Scatter(x=x, y=source_b, mode='lines', name='Source B')
    
    figure = {'data': [trace_b],
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Sources', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }

    return figure

@app.callback(Output('source-C', 'figure'),
                [Input('freq-slider-C', 'value')])   
def update_sources_plot(freq_c):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 10, 500)
    source_c = np.sin(freq_c * x)
    trace_c = go.Scatter(x=x, y=source_c, mode='lines', name='Source C')
    
    figure = {'data': [trace_c],
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Sources', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }

    return figure


if __name__ == '__main__':
    app.run(debug=True)