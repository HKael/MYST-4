"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import numpy as np
import datetime

import functions_PyMetatrader5 as fnmt5


def validadiciones(df_index: pd.DataFrame, mt5_client, symbol):
    # semilla
    np.random.seed(545)
    # 5 fechas aleatorioas
    escenarios = np.random.choice([i for i in range(len(df_index))], 5)
    # Agregamos media hora a todas las fechas
    tf = datetime.timedelta(hours=0.5)
    # Ajusta para daylight savings
    dates = [[df_index.iloc[i].name, df_index.iloc[i].name + tf] for i in escenarios]

    # descarga de precios
    prices = [fnmt5.f_hist_prices(mt5_client, [symbol], 'M1', dates[i][0], dates[i][-1]).get(symbol) for i in
              range(len(dates))]

    # separacion y columnas de tiempo
    escenario1 = prices[0]
    escenario1['time'] = [datetime.datetime.utcfromtimestamp(times) for times in escenario1['time']]

    escenario2 = prices[1]
    escenario2['time'] = [datetime.datetime.utcfromtimestamp(times) for times in escenario2['time']]

    escenario3 = prices[2]
    escenario3['time'] = [datetime.datetime.utcfromtimestamp(times) for times in escenario3['time']]

    escenario4 = prices[3]
    escenario4['time'] = [datetime.datetime.utcfromtimestamp(times) for times in escenario4['time']]

    escenario5 = prices[4]
    escenario5['time'] = [datetime.datetime.utcfromtimestamp(times) for times in escenario5['time']]

    return escenario1, escenario2, escenario3, escenario4, escenario5
