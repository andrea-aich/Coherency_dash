import dash
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from scipy.fftpack import fft, fftn
from scipy.signal.windows import hann


# Initialize the app
app = dash.Dash(__name__,
                external_scripts=['https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'])
app.config.suppress_callback_exceptions = True


app.layout = html.Div(className='big-app-container',
    children=[
        html.Div(className='banner', children=[
            html.Div(className='banner-text',children=[
                html.H1('DASH - COHERENCY'),
                html.P('Visualising time series with Plotly - Dash.')],
        ),
        ]),
        html.Div(className='app-container',
            children=[
                html.Div(className='status-container',
                    children=[
                        html.Div(className='row div-Create-your-sources',
                            children=[
                                html.Div(className='explanation text',
                                        children=[
                                            html.H2('Create your sources.'),
                                            html.P('They are like the ingredients of your cake that you will later mix together.'),
                                            html.P('Use the sliders to change the frequency of the sources.'),
                                         ]
                                ),
                                html.Div(className='row three-sources',
                                        children=[
                                            html.Div(className='four columns source A', children=[
                                                html.Div(className='div-slider-A',
                                                    children=[
                                                        html.P('Frequency A (Hz)'),
                                                        dcc.Slider(id='freq-slider-A', min=0, max=100, step=1, value=10,
                                                            marks={i: '{}'.format(i) for i in range(0, 101, 10)}),
                                                        dcc.Graph(id='source-A',
                                                            config={'displayModeBar': False},
                                                            animate=True)
                                                    ]
                                                )    
                                            ]),
                                            html.Div(className='four columns source B', children=[
                                                html.Div(className='div-slider-B',
                                                    children=[
                                                        html.P('Frequency B (Hz)'),
                                                        dcc.Slider(id='freq-slider-B', min=0, max=100, step=1, value=40,
                                                            marks={i: '{}'.format(i) for i in range(0, 101, 10)}),
                                                        dcc.Graph(id='source-B',
                                                            config={'displayModeBar': False},
                                                            animate=True)
                                                    ]
                                                )    
                                            ]),
                                            html.Div(className='four columns source C', children=[
                                                html.Div(className='div-slider-C',
                                                    children=[
                                                        html.P('Frequency C (Hz)'),
                                                        dcc.Slider(id='freq-slider-C', min=0, max=100, step=1, value=4,
                                                            marks={i: '{}'.format(i) for i in range(0, 101, 10)}),
                                                        dcc.Graph(id='source-C',
                                                            config={'displayModeBar': False},
                                                            animate=True)
                                                    ]
                                                )    
                                            ]),
                                        ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(className='graphs-container build-sources',
            children=[ 
                html.Div(className='row top-section-container',
                    children=[
                        html.Div(className='nine columns',
                            children=[
                                html.H2('Combine your sources to build your signal.'),
                                html.Div(style={'padding': '10px', 'margin': '10px'}, children=[
                                    dcc.Markdown('''
                                        Signal $x(t)$ is fixed and computed with the following formula: 
                                        $$
                                        x(t) = s_A(t) + s_B(t) + s_C(t)
                                        $$

                                        Signal y(t) is computed as a weighted sum of the sources with an added noise component:
                                        $$
                                        y(t) = w_1 s_A(t) + w_2 s_B(t) + w_3 s_C(t) + \\epsilon
                                        $$
                                        
                                    ''', mathjax=True)
                                ]),
                                html.P('Use the sliders to choose the weights, phase shift and noise level.'),
                                html.Div(className='row signal A', children=[
                                    html.Div(className='row div-signals-sliders',
                                        children=[
                                            html.Div(className='two columns div-source-A', children=[ 
                                                html.P('Weight of source A'),
                                                dcc.Slider(id='source-A-slider', min=0, max=4, step=0.25, value=1,
                                                    marks={i: '{}'.format(i) for i in range(0, 5)})]),
                                            html.Div(className='two columns div-source-B', children=[
                                                html.P('Weight of source B'),
                                                dcc.Slider(id='source-B-slider', min=0, max=4, step=0.25, value=1,
                                                    marks={i: '{}'.format(i) for i in range(0, 5)})]),  
                                            html.Div(className='two columns div-source-C', children=[
                                                html.P('Weight of source C'),
                                                dcc.Slider(id='source-C-slider', min=0, max=4, step=0.25, value=1,
                                                    marks={i: '{}'.format(i) for i in range(0, 4)})]),
                                            html.Div(className='two columns div-noise', children=[
                                                html.P('Noise level'),
                                                dcc.Slider(id='noise-slider', min=0, max=4, step=1, value=1,
                                                    marks={i: '{}'.format(i) for i in range(0, 5)})]), 
                                            html.Div(className='two columns div-phase', children=[
                                                html.P('Phase shift of source B'),
                                                dcc.Slider(id='phase-slider', min=0, max=2*np.pi, step=0.25, value=1,
                                                    marks={i: '{}'.format(i) for i in range(0, 6)})
                                                ])
                                        ]
                                    ),
                                    html.Div(className='div-signals-plot',
                                    children=[
                                        dcc.Graph(id='signals-plot',
                                            config={'displayModeBar': False},
                                            animate=True)
                                    ]
                                    )    
                                ])
                            ]
                        ),
                        html.Div(className='three columns div-coherency',
                            children=[
                                html.H2('Compute coherency'),
                                html.Div(style={'padding': '10px', 'margin': '10px'}, children=[
                                    dcc.Markdown('''
                                        Coherency $C_{xy}(f)$ is computed with the following formula: 
                                        $$
                                        C_{xy}(f) = \\frac{S_{xy}(f)}{\\sqrt{S_{xx}(f) S_{yy}(f)}}
                                        $$

                                        Where $S_{xy}(f)$ is the cross-spectral density between signals $x(t)$ and $y(t)$, and $S_{xx}(f)$ and $S_{yy}(f)$ are the auto-spectral densities of $x(t)$ and $y(t)$ respectively.
                                    ''', mathjax=True)
                                ]),
                                html.P('Use the sliders to choose the frequency.'),
                                dcc.Slider(id='coherency-freq-slider', min=1, max=100, step=1, value=50,
                                    marks={i: '{}'.format(i) for i in range(0, 101, 10)}),   
                                dcc.Graph(id='coherency-plot',
                                    config={'displayModeBar': False},
                                    animate=False)
                            ]
                        )
                    ]
                )
            ]
        ),
        
                 
        html.Script('''
            console.log("MathJax v3 Initialization Script");
            
            function processMathJax() {
                console.log("Processing MathJax");
                if (window.MathJax && window.MathJax.typesetPromise) {
                    console.log("Calling typesetPromise");
                    MathJax.typesetPromise().catch(err => console.log("MathJax error:", err));
                }
            }
            
            // Wait for MathJax to be ready
            window.MathJax = {
                startup: {
                    pageReady: () => {
                        console.log("MathJax page ready");
                        processMathJax();
                    }
                }
            };
            
            // Also try after page load
            window.addEventListener('load', function() {
                console.log("Window load event fired");
                setTimeout(processMathJax, 1000);
            });
        ''')
    ]
)


@app.callback(Output('output', 'children'), Input('input', 'value'))
def display_output(value):
    return 'You have entered {}'.format(value)

# trying my own callback for the sliders
@app.callback(Output('source-A', 'figure'),
                [Input('freq-slider-A', 'value')])   
def update_sources_plot(freq_a):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 1000, 1000)
    source_a = np.sin(freq_a*2*np.pi/Fs * x)
    trace_a = go.Scatter(x=x, y=source_a, mode='lines', name='Source A')
    figure = {'data': [trace_a],
              'layout': go.Layout(
                  #template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  title={'text': 'Source A', 'x': 0.5},
              ),
              }

    return figure


@app.callback(Output('source-B', 'figure'),
                [Input('freq-slider-B', 'value')])   
def update_sources_plot(freq_b):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 1000, 1000)
    source_b = np.sin(freq_b*2*np.pi/Fs * x)
    trace_b = go.Scatter(x=x, y=source_b, mode='lines', name='Source B')
    
    figure = {'data': [trace_b],
              'layout': go.Layout(
                  #template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  title={'text': 'Source B',  'x': 0.5},
              ),
              }

    return figure

@app.callback(Output('source-C', 'figure'),
                [Input('freq-slider-C', 'value')])   
def update_sources_plot(freq_c):
    ''' Draw traces of the feature 'change' based one the currently selected frequencies '''
    x = np.linspace(0, 1000, 1000)
    source_c = np.sin(freq_c*2*np.pi/Fs * x)
    trace_c = go.Scatter(x=x, y=source_c, mode='lines', name='Source C')
    
    figure = {'data': [trace_c],
              'layout': go.Layout(
                  #template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  title={'text': 'Source C',  'x': 0.5},
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
    t = np.linspace(0,total_time*Fs,total_time*Fs,endpoint=True) # time points in miliseconds, 10 seconds at 1000 Hz
    freq1 = freq1_val # Hz, first frequency
    freq2 = freq2_val # Hz, second frequency 
    freq3 = freq3_val # Hz, third frequency
    
    s1t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq1/Fs) # signal 1
    s2t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)) # signal 2
    s3t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*t*freq3/Fs) # signal 3
    
    return t,s1t,s2t,s3t

def update_signals(phase_val, noise_val, s1_weight, s2_weight, s3_weight, s1t, s2t, s3t, freq2, num_trials=1):
    noise_coef = noise_val # noise coefficient
    t = np.linspace(0,total_time*Fs,total_time*Fs,endpoint=True) # time points in miliseconds, 10 seconds at 1000 Hz
    
    phase_shift = phase_val*2*np.pi # in radians
    
    s2_1t = s2t
    s2_2t = np.ones((num_trials,total_time*Fs))*np.sin(2*np.pi*(t*freq2/Fs)+ phase_shift) # signal 2 with phase shift
    
    Xt = s1t + s2_1t + s3t
    Yt = s1_weight*s1t + s2_weight*s2_2t + s3_weight*s3t + noise_coef*np.random.randn(num_trials,total_time*Fs)
    return t,Xt,Yt

def coherency(time,f,Xt,Yt,Fs,T):
    C_xy_f_t = ()
    trials = np.shape(Xt)[0]
    H_window = np.ones((trials,T))*hann(T)
    # First we convert f to columns according to the resolution of our fft
    w = int(f/freq_res)
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
    tt, s1t, s2t, s3t = update_sources(
        slider_freq_A,
        slider_freq_B,
        slider_freq_C,
        num_trials
    )
    tt, Xt, Yt = update_signals(slider_phase,slider_noise, slider_source_A, slider_source_B, slider_source_C,s1t, s2t, s3t, slider_freq_B, num_trials)

    trace_a = go.Scatter(x=tt, y=Xt[0,:] , mode='lines', name='Signal X')
    trace_b = go.Scatter(x=tt, y=Yt[0,:] , mode='lines', name='Signal Y')

    figure = {'data': [trace_a, trace_b],
              'layout': go.Layout(
                  #template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=200,
                  hovermode='x',
                  autosize=True,
                  xaxis_title="Time [ms]",
                  yaxis_showticklabels=False,
                  yaxis_showgrid=False,
                  title={'text': 'Signals',  'x': 0.5},
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
    tt, s1t, s2t, s3t = update_sources(
        slider_freq_A,
        slider_freq_B,
        slider_freq_C,
        num_trials
    )
    tt, Xt, Yt = update_signals(slider_phase,slider_noise, slider_source_A, slider_source_B, slider_source_C,s1t, s2t, s3t, slider_freq_B, num_trials)

    cohe = coherency(total_time, coherency_freq, Xt, Yt,Fs,T)
    Cxy_f = np.mean(cohe)
    

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


    # For coherency values per trial
    x_vals = []
    y_vals = []

    for r, i in zip(np.real(cohe), np.imag(cohe)):
        x_vals += [0, r]
        y_vals += [0, i]

    trace_c = go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines+markers"
    )

    my_cirle = go.Scatter(
        x=np.cos(np.linspace(0, 2*np.pi, 100)),
        y=np.sin(np.linspace(0, 2*np.pi, 100)),
        mode="lines",
        name="Unit Circle"
    )

    figure = {'data': [trace_a, trace_b, trace_c, my_cirle],
              'layout': go.Layout(
                  #template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  width=310,
                  hovermode='x',
                  autosize=True,
                  xaxis_showticklabels=False,
                  xaxis_showgrid=False,
                  yaxis_showticklabels=False,
                  yaxis_showgrid=False,
                  title={'text': 'Coherency',  'x': 0.5},
                  legend=dict(y=-2,x=0)
              ),
            }

    return figure

if __name__ == '__main__':
    app.run(debug=True)