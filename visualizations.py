
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

def candle_stick_plot(df: pd.DataFrame):

    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                          open=df['open'], high=df['high'], low=df['low'], close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.update_layout(title='USD/CHF')

    fig.show()