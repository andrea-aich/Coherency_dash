import dash
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from scipy.fftpack import fft, fftn
from scipy.signal.windows import hann

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
        html.Div(className='row',
                    children=[
                        html.Div(className='column left div-Create-your-sources',
                                    children=[
                                        html.H2('Create your sources.'),
                                        html.P('They are like the ingredients of your cake that you will later mix together.'),
                                        html.P('Use the sliders to change the frequency of the sources.'),
                        html.Div(className='row source A', children=[
                            html.Div(className='column left div-slider-A',
                                 children=[
                                    html.P('Frequency A'),
                                    dcc.Slider(id='freq-slider-A', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='column right div-sources-plot-A',
                                 children=[
                                     dcc.Graph(id='source-A',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                        html.Div(className='row source B', children=[
                            html.Div(className='column left div-slider-B',
                                 children=[
                                    html.P('Frequency B'),
                                    dcc.Slider(id='freq-slider-B', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='column right div-sources-plot-B',
                                 children=[
                                     dcc.Graph(id='source-B',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                        html.Div(className='row source C', children=[
                            html.Div(className='column left div-slider-C',
                                 children=[
                                    html.P('Frequency C'),
                                    dcc.Slider(id='freq-slider-C', min=0, max=2*np.pi, step=0.25, value=np.pi / 2,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),
                                ]),
                            html.Div(className='column right',
                                 children=[
                                     dcc.Graph(id='source-C',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ]),
                    ]
                ),
        html.Div(className='column right',
                    children=[
                        html.H2('Combine your sources to build your signals.'),
                        html.P('Use the sliders to choose the frequency and time window.'),
                        html.Div(className='row signal A', children=[
                            html.Div(className='column right div-single-sliders',
                                 children=[
                                    html.P('Weight of source A'),
                                    dcc.Slider(id='source-A-slider', min=0, max=10, step=0.25, value=1,
                                           marks={i: '{}'.format(i) for i in range(0, 11)}),
                                    html.P('Weight of source B'),
                                    dcc.Slider(id='source-B-slider', min=0, max=10, step=0.25, value=1,
                                           marks={i: '{}'.format(i) for i in range(0, 11)}),  
                                    html.P('Weight of source C'),
                                    dcc.Slider(id='source-C-slider', min=0, max=10, step=0.25, value=1,
                                           marks={i: '{}'.format(i) for i in range(0, 11)}),            
                                    html.P('Noise level'),
                                    dcc.Slider(id='noise-slider', min=0, max=100, step=10, value=1,
                                           marks={i: '{}'.format(i) for i in range(0, 11)}), 
                                    html.P('Phase shift between source B and source C'),
                                    dcc.Slider(id='phase-slider', min=0, max=2*np.pi, step=0.25, value=1,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),         
                                ]),
                            html.Div(className='column right div-signals-plot',
                                 children=[
                                     dcc.Graph(id='signals-plot',
                                     config={'displayModeBar': False},
                                     animate=True)
                                    ])    
                        ])
                    ]
                )
                    ]
        ),       
        html.Div(className='row',
                    children=[
                        html.Div(className='eight columns div-coherency',
                                    children=[
                                        html.H2('Compute coherency'),
                                        html.P('Use the sliders to choose the frequency.'),
                                        dcc.Slider(id='coherency-freq-slider', min=0, max=2*np.pi, step=0.25, value=np.pi,
                                           marks={i: '{}'.format(i) for i in range(0, 6)}),   
                                        dcc.Graph(id='coherency-plot',
                                     config={'displayModeBar': False},
                                     animate=False)
                                    ]
                                )
                    ]
                ),
        html.Div(className='row',
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
                                ]
                             )                               
                    ]
                 )
    ]
)


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
    print('entered update_sources_plot for source A')
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

total_time = 5  # in seconds: time of recording per trial
Fs = 1000 # in Hertz: sampling frequency
T = 1000 # in ms: time of an epoch

# We can already calculate the interrelationships between time and frequency domains
freq_res = 1/(T/1000) # frequency resolution
N = Fs*(T/1000) # number of samples in an epoch
Fmax = (N/2)*freq_res # maximal frequency or nyquist frequency
W = np.linspace(0,Fmax,T)*freq_res # here we store the frequency indices

# For the statistics
num_trials = 10 

def sources(phase_val, noise_val, freq1_val, freq2_val, freq3_val, num_trials=1):
    noise_coef = noise_val # noise coefficient
    t = np.linspace(0,total_time*Fs,total_time*Fs,endpoint=True) # time points in miliseconds, 10 seconds at 1000 Hz
    freq1 = freq1_val # Hz, first frequency
    freq2 = freq2_val # Hz, second frequency 
    freq3 = freq3_val # Hz, third frequency
    
    phase_shift = phase_val*2*np.pi # in radians
    
    s1t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq1/Fs) # signal 1
    s2_1t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)) # signal 2
    s2_2t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)+ phase_shift) # signal 2 with phase shift
    s3t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq3/Fs) # signal 3
    
    alpha = np.ones((num_trials,total_time*Fs))*np.linspace(-1,1,total_time*Fs,endpoint=True)
    alpha = np.sign(alpha) +1
    beta = np.sign(-alpha) +1
    Xt = s1t + 1.5*s2_1t + s3t + noise_coef*np.random.randn(num_trials,total_time*Fs)
    Yt = 0.5*s1t + alpha*s2_2t + beta*s2_1t + noise_coef*np.random.randn(num_trials,total_time*Fs)
    return t,Xt,Yt,s1t,s2_1t,s2_2t,s3t,alpha,beta

def update_sources(freq1_val, freq2_val, freq3_val, num_trials=1):
    print('entered update_sources')
    t = np.linspace(0,total_time*Fs,total_time*Fs,endpoint=True) # time points in miliseconds, 10 seconds at 1000 Hz
    freq1 = freq1_val # Hz, first frequency
    freq2 = freq2_val # Hz, second frequency 
    freq3 = freq3_val # Hz, third frequency
    
    s1t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq1/Fs) # signal 1
    s2t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)) # signal 2
    s3t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq3/Fs) # signal 3
    
    return t,s1t,s2t,s3t

def update_signals(phase_val, noise_val, s1_weight, s2_weight, s3_weight, s1t, s2t, s3t, freq2, num_trials=1):
    print('entered update_signals')
    noise_coef = noise_val # noise coefficient
    t = np.linspace(0,total_time*Fs,total_time*Fs,endpoint=True) # time points in miliseconds, 10 seconds at 1000 Hz
    
    phase_shift = phase_val*2*np.pi # in radians
    
    s2_1t = s2t
    s2_2t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)+ phase_shift) # signal 2 with phase shift
    
    alpha = np.ones((num_trials,total_time*Fs))*np.linspace(-1,1,total_time*Fs,endpoint=True)
    alpha = np.sign(alpha) +1
    beta = np.sign(-alpha) +1
    Xt = s1t + s2_1t + s3t + noise_coef*np.random.randn(num_trials,total_time*Fs)
    Yt = s1_weight*s1t + s2_weight*(alpha*s2_2t + beta*s2_1t) + s3_weight*s3t + noise_coef*np.random.randn(num_trials,total_time*Fs)
    return t,Xt,Yt

def coherency(time,f,Xt,Yt,Fs=1000,T=500):
    print('entered coherency')
    C_xy_f_t = ()
    trials = np.shape(Xt)[0]
    H_window = np.ones((trials,T))*hann(T)
    # First we convert f to columns according to the resolution of our fft
    w = int(f/freq_res)
    
    print('time: ',time)
    print('Fs: ',Fs)
    print('T: ',T)
    for segs in range(int(np.floor(time*Fs/T))):
        #Making a matrix of the segments of Xt and Yt during a specific time through all trials
        X = Xt[:,segs*T:(segs+1)*T]
        Y = Yt[:,segs*T:(segs+1)*T]

        n_freq = int(time * Fs // T)
        Xf = np.zeros((n_freq, int(T)), dtype="complex_")
        Yf = np.zeros((n_freq, int(T)), dtype="complex_")

        Xf=fftn(X*H_window)
        Yf=fftn(Y*H_window)
        
        # We approximate the expectation value with the mean over all the epochs
        # We will take a narrow band to include +-2 Hz around f
        S_xy_f_t = np.mean(Xf[:,w-1:w+1]*np.conj(Yf[:,w-1:w+1]))
        S_xx_f_t = np.mean(Xf[:,w-1:w+1]*np.conj(Xf[:,w-1:w+1]))
        S_yy_f_t = np.mean(Yf[:,w-1:w+1]*np.conj(Yf[:,w-1:w+1]))

        # We now construct the denominator of the coherency
        deno_f_t = np.sqrt(np.real(S_xx_f_t*S_yy_f_t))
        
        # We finally get the coherency
        C_xy_f_t = np.append(C_xy_f_t,S_xy_f_t/deno_f_t)
        print(deno_f_t,C_xy_f_t)
        
    return C_xy_f_t


def regraph2(slider_phase, slider_noise, slider_freq1, slider_freq2, slider_freq3, slider_f):

    tt, Xt, Yt, s1t, s2_1t, s2_2t, s3t, alpha, beta = sources(
        slider_phase/100,
        slider_noise/100,
        slider_freq1,
        slider_freq2,
        slider_freq3,
        num_trials
    )

    xt = Xt[0, :]
    yt = Yt[0, :]

    cohe = coherency(total_time, slider_f, Xt, Yt)
    Cxy_f = np.mean(cohe)

    # Phase angles
    angles = np.arctan2(np.imag(cohe), np.real(cohe))


# trying my own callback for the sliders of the signals
@app.callback(Output('signals-plot', 'figure'),
                [Input('source-A-slider', 'value'),
                 Input('source-B-slider', 'value'),
                 Input('source-C-slider', 'value'),
                 Input('noise-slider', 'value'),
                 Input('phase-slider', 'value'),
                 Input('freq-slider-A', 'value'),
                 Input('freq-slider-B', 'value'),
                 Input('freq-slider-C', 'value')])   
def update_signals_plot(slider_source_A, slider_source_B, slider_source_C, slider_noise, slider_phase, slider_freq_A, slider_freq_B, slider_freq_C):
    ''' Draw traces of the feature 'change' based on the currently selected frequencies '''
    print('slider_source_A: ', slider_source_A)
    tt, s1t, s2t, s3t = update_sources(
        slider_freq_A,
        slider_freq_B,
        slider_freq_C,
        num_trials
    )
    tt, Xt, Yt = update_signals(slider_phase,slider_noise, slider_source_A, slider_source_B, slider_source_C,s1t, s2t, s3t, slider_freq_B, num_trials)

    print('tt[0:10]: ', tt[0:10])
    print('Xt[0,:][0:10]]: ', Xt[0,:][0:10])
    trace_a = go.Scatter(x=tt, y=Xt[0,:] , mode='lines', name='Signal A')
    trace_b = go.Scatter(x=tt, y=Yt[0,:] , mode='lines', name='Signal B')

    figure = {'data': [trace_a, trace_b],
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  yaxis_showticklabels=False,
                  yaxis_showgrid=False,
                  title={'text': 'Sources', 'font': {'color': 'white'}, 'x': 0.5},
              ),
            }

    return figure

# Now for the coherency finally 
@app.callback(Output('coherency-plot', 'figure'),
                [Input('coherency-freq-slider', 'value'),
                Input('source-A-slider', 'value'),
                Input('source-B-slider', 'value'),
                Input('source-C-slider', 'value'),
                Input('noise-slider', 'value'),
                Input('phase-slider', 'value'),
                Input('freq-slider-A', 'value'),
                Input('freq-slider-B', 'value'),
                Input('freq-slider-C', 'value')
                ])
               
def update_everything_plot(coherency_freq, slider_source_A, slider_source_B, slider_source_C, slider_noise, slider_phase, slider_freq_A, slider_freq_B, slider_freq_C):
    ''' Draw traces of the feature 'change' based on the currently selected frequencies '''
    print('slider_source_A: ', slider_source_A)
    tt, s1t, s2t, s3t = update_sources(
        slider_freq_A,
        slider_freq_B,
        slider_freq_C,
        num_trials
    )
    tt, Xt, Yt = update_signals(slider_phase,slider_noise, slider_source_A, slider_source_B, slider_source_C,s1t, s2t, s3t, slider_freq_B, num_trials)

    cohe = coherency(total_time, coherency_freq, Xt, Yt)
    Cxy_f = np.mean(cohe)
    print('Cxy_f: ', Cxy_f)

    # Phase angles
    angles = np.arctan2(np.imag(cohe), np.real(cohe))

    # FIGURE 3: Mean Coherency
    
    trace_a = go.Scatter(
        x=[np.real(Cxy_f)],
        y=[np.imag(Cxy_f)],
        mode="markers",
        name="Mean Cxy"
    )
    trace_b = go.Scatter(
        x=[0, np.real(Cxy_f)],
        y=[0, np.imag(Cxy_f)],
        mode="lines",
        name="Vector"
    )

    figure = {'data': [trace_a, trace_b],
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  yaxis_showticklabels=False,
                  yaxis_showgrid=False,
                  title={'text': 'Sources', 'font': {'color': 'white'}, 'x': 0.5},
              ),
            }

    return figure

if __name__ == '__main__':
    app.run(debug=True)