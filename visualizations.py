
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def candle_stick_plot(df: pd.DataFrame):

    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                          open=df['open'], high=df['high'], low=df['low'], close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.update_layout(title='USD/CHF')

    fig.show()

def opt_no_opt(opt, no_opt):
    fig = go.Figure(go.Scatter(x=date, y=capital, name='Optimizado', line=dict(color='red')))
    capital = opt['capital_acm']
    date = opt.index
    fig.add_trace(x=date, y=capital, name='Optimizado', line=dict(color='red'))

    fig.add_trace(x=date, y=no_opt['capital_acm'], name='No optimizado', line=dict(color='blue'))
    fig.show()

import plotly.graph_objects as go


def graph_comp(evol,evol2):


    evol = pd.DataFrame(evol['capital_acm'])
    evol = evol.sort_index()

    #------------------------ Obtencion de los datos
    # Datos evol capital
    x= (evol.index)
    y = np.array(evol['capital_acm'])


    evol2 = pd.DataFrame(evol2['capital_acm'])
    evol2 = evol2.sort_index()

    #------------------------ Obtencion de los datos
    # Datos evol capital
    x2= (evol2.index)
    y2 = np.array(evol2['capital_acm'])



    #---------------------------------------------- Grafica
    fig = go.Figure()
    # Evolucion del capital
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name = 'backtest_opt',
        marker=dict( color='black',size=10),
        line=dict(color='black', width=4)
    ))
    
    
    # Evolucion del capital
    fig.add_trace(go.Scatter(
        x=x2,
        y=y2,
        name = 'df_backtest',
        marker=dict( color='green',size=10),
        line=dict(color='green', width=4)
    ))

   

    fig.update_layout(title='Evolución del capital',
                       xaxis_title='Fecha',
                       yaxis_title='Capital')

    return fig.show()
