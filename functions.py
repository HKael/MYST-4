"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import grubbs as grubbs
import pandas as pd
import numpy as np
import datetime

from matplotlib import pyplot, pyplot as plt
from scipy.stats import shapiro
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import scikit_posthocs as sp
import statsmodels.api as sm

import functions_PyMetatrader5 as fnmt5


def validadiciones(df_index: pd.DataFrame, mt5_client, symbol):
    # semilla
    np.random.seed(545)
    # 5 fechas aleatorioas
    validaciones = np.random.choice([i for i in range(len(df_index))], 5)
    # Agregamos media hora a todas las fechas
    tf = datetime.timedelta(hours=0.5)
    # Ajusta para daylight savings
    dates = [[df_index.iloc[i].name, df_index.iloc[i].name + tf] for i in validaciones]

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


def escenarios(fila):
    if fila[0] >= fila[1] >= fila[2]:
        escenario = 'A'
    elif fila[0] >= fila[1] < fila[2]:
        escenario = 'B'
    elif fila[0] < fila[1] >= fila[2]:
        escenario = 'C'
    else:
        escenario = 'D'
    return escenario


def func_df_escenarios(indice: pd.DataFrame, symbol, mt5_client):
    df_escenarios_f = pd.DataFrame(index=indice.index)
    df_escenarios_f['Escenario'] = [escenarios(indice.iloc[i].to_list()) for i in range(len(indice))]

    tf = datetime.timedelta(hours=0.5)
    dst_adjust = datetime.timedelta(hours=1)

    dates = [df_escenarios_f.iloc[i].name - tf + dst_adjust for i in range(len(df_escenarios_f))]

    prices = [fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', dates[i], 61).get(symbol) for i in
              range(len(dates))]

    pip_size = 10000
    direccion = []
    pip_alcistas = []
    pip_bajistas = []
    vol = []
    for i in range(len(df_escenarios_f)):
        # Para cada uno de los precios
        df = prices[i]
        # Convertir columnas de tiempo
        df['time'] = [datetime.datetime.utcfromtimestamp(times) for times in df['time']]
        # Direccion
        direc = df['close'].iloc[-1] - df['open'].iloc[30]
        # Validaciòn de direcciòn
        if direc <= 0:
            direccion.append(1)
        else:
            direccion.append(-1)
        # Pips alcistas
        high = (df['high'].iloc[30:-1].max() - df['open'].iloc[30]) * pip_size
        # Pips bajistas
        low = (df['open'].iloc[30] - df['low'].iloc[30:-1].min()) * pip_size
        # volatilidad
        vola = (df['high'].max() - df['low'].min()) * pip_size

        pip_alcistas.append(high)
        pip_bajistas.append(low)
        vol.append(vola)

    df_escenarios_f['Direccion'] = direccion
    df_escenarios_f['pip_alcistas'] = pip_alcistas
    df_escenarios_f['pips_bajistas'] = pip_bajistas
    df_escenarios_f['volatilidad'] = vol

    return df_escenarios_f


# %% Statistical aspect


def acf(param_data):
    plt.rcParams["figure.figsize"] = (16, 6)
    plot_acf(param_data)
    return


def pacf(param_data):
    plt.rcParams["figure.figsize"] = (16, 6)
    plot_pacf(param_data)
    return


def regression(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    print(model.summary())
    return


def regression_v(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    B0 = model.params[0]
    B1 = model.params[1]
    x = x[:, 1]
    x2 = np.linspace(x.min(), x.max(), 100)
    y_hat = x2 * B1 + B0
    plt.scatter(x, y)
    plt.plot(x2, y_hat, "r")
    return


def heteroskedasticity(param_data):
    summ = sm.OLS(param_data.index, param_data["Actual"]).fit()
    comp = param_data[["Actual", "Consensus"]]
    bp_test = het_breuschpagan(summ.resid, comp)
    print('LM Statistic: %f' % bp_test[0])
    print('LM Statistic p-value: %f' % bp_test[1])
    print('F-Statistic: %f' % bp_test[2])
    print('F-Statistic p-value: %f' % bp_test[3])
    if bp_test[1] < 0.05:
        print("Heteroskedasticity is indicated if p <0.05, so according to these tests, this model is heteroskedastic.")
    else:
        print("Heteroskedasticity is indicated if p <0.05, so according to these tests, this model is not "
              "heteroskedastic.")
    return


def norm_test(param_data):
    stat, p = shapiro(param_data)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
        print(" Sample has normal distribution")
    else:
        print('Sample does not look Gaussian (reject H0)')
        print("Sample does not have normal distribution")
    return


def stationarity(param_data):
    X = param_data.values
    result = adfuller(X)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    if result[1] > 0.05:
        print("No stationarity detected")
    else:
        print("Stationarity detected")
    return


def seasonality(param_data):
    plt.rcParams["figure.figsize"] = (12, 12)
    decomposition = sm.tsa.seasonal_decompose(param_data, model='additive', period=12)
    decomposition.plot()
    return plt.show()


def outlier_v(param_data):
    plt.rcParams["figure.figsize"] = (16, 8)
    plt.boxplot(param_data)
    plt.title("Outlier Value Boxplot Visual Detection")
    plt.show()
    if len(param_data) == len(sp.outliers_grubbs(param_data)):
        print("No outliers detected")
    else:
        print("Outlier detected")
    return


def op(timestamp, initial, final, maxp, minp, position, tp, sl):
    if position == 'Buy':
        tp = initial + tp / 10000
        sl = initial - sl / 10000
    else:
        tp = initial - tp / 10000
        sl = initial + sl / 10000

    df = pd.DataFrame(
        {'Operation Parameter': ['TimeStamp', 'Window', 'Initial Price', 'Final Price', 'Maximum Price', 'Minimum Price',
                            'Stop Loss', 'Take Profit', 'Volume', 'Capital', 'Position'],
         'Operation Value': [timestamp, '00:30:00', '$ ' + str(initial), '$ ' + str(final), '$ ' + str(maxp),
                             '$ ' + str(minp),
                             "$ " + str(sl), "$ " + str(tp), int(1000 / initial), '1000 USD', position], })
    return df
