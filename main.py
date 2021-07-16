"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# %%
import pandas as pd
import numpy as np
import functions_PyMetatrader5 as fnmt5
import functions as fn
import visualizations as vs
import pyswarms as ps

# %%
# Archivo con el índice a usar
indice = pd.read_csv('files\\Unemployment Rate - United States.csv', index_col='DateTime')
# Eliminar columan de revised
indice.drop('Revised', axis=1, inplace=True)
# Convertir a datetime la columna de fechas
indice.index = pd.to_datetime(indice.index)

# Faltante en previous
indice.iloc[-1]['Previous'] = indice.iloc[-2]['Actual']

# %%
# Ejecutables
# local_exe = 'C:\\Program Files\\MetaTrader 5\\terminal64.exe'
# local_exe = 'C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe'
local_exe = 'C:\\Archivos de programa\\MetaTrader 5 Terminal\\terminal64.exe'

# Número de cuenta
mt5_acc = 5383442
# Contraseña
mt5_pass = "44GxKTtf"
# Inicialización de mt5
mt5_client = fnmt5.f_init_login(mt5_acc, mt5_pass, local_exe)

# Escenarios para validaciones visuales
symbol = 'USDCHF'
escenario1, escenario2, escenario3, escenario4, escenario5 = fn.validadiciones(indice, mt5_client, symbol)

# Graficos de velas para cada escenario
vs.candle_stick_plot(escenario1)
vs.candle_stick_plot(escenario2)
vs.candle_stick_plot(escenario3)
vs.candle_stick_plot(escenario4)
vs.candle_stick_plot(escenario5)

# DataFrame escenarios

df_escenarios, precios = fn.func_df_escenarios(indice, symbol, mt5_client)

# %%
# Prueba y entrenamiento
indice_prueba = indice.iloc[0:13, :]
indice_train = indice.iloc[13:26, :]

escenarios_prueba = df_escenarios.iloc[0:13, :]
escenarios_test = df_escenarios.iloc[13:26, :]

# analisis escenarios test
escenarios_conteodirec = escenarios_test.groupby(['Escenario', 'Direccion'])['Direccion'].count()
escenarios_conteopipa = escenarios_test.groupby(['Escenario', 'Direccion'])['pip_alcistas'].median()
escenarios_conteopipamax = escenarios_test.groupby(['Escenario', 'Direccion'])['pip_alcistas'].max()
escenarios_conteopipb = escenarios_test.groupby(['Escenario', 'Direccion'])['pips_bajistas'].median()
escenarios_conteopipbmax = escenarios_test.groupby(['Escenario', 'Direccion'])['pips_bajistas'].max()
escenarios_conteovol = escenarios_test.groupby(['Escenario', 'Direccion'])['volatilidad'].median()

escenarioa = ['compra', 14, 12, 80]
escenariob = ['venta', 8, 5, 200]
escenarioc = ['compra', 15, 9, 110]
escenariod = ['compra', 7, 4, 250]

df_decisiones = pd.DataFrame(columns=['escenario', 'operacion', 'sl', 'tp', 'volumen'], index=[0, 1, 2, 3])
df_decisiones.iloc[0] = ['A'] + escenarioa
df_decisiones.iloc[1] = ['B'] + escenariob
df_decisiones.iloc[2] = ['C'] + escenarioc
df_decisiones.iloc[3] = ['D'] + escenariod


def decisiones(operacion, sl, tp, volumen):

    df_decisiones = pd.DataFrame(columns=['escenario', 'operacion', 'sl', 'tp', 'volumen'],
                                 index=[0, 1, 2, 3])
    df_decisiones['escenario'] = ['A', 'B', 'C', 'D']
    df_decisiones['operacion'] = operacion
    df_decisiones['sl'] = sl
    df_decisiones['tp'] = tp
    df_decisiones['volumen'] = volumen
    return df_decisiones


def backtest(df_decisiones):
    df_backtest = pd.DataFrame(columns=['escenario', 'operacion', 'volumen', 'resultado', 'pips',
                                        'capital', 'capital_acm'], index=escenarios_test.index)

    df_backtest['escenario'] = escenarios_test['Escenario']

    operacion = []
    volumen = []
    resultado = []
    pips = []
    capital = []

    for i in range(len(escenarios_test)):

        if escenarios_test['Escenario'].iloc[i] == 'A':
            operacioni = df_decisiones['operacion'].iloc[0]
            operacion.append(operacioni)
            volumeni = df_decisiones['volumen'].iloc[0]
            volumen.append(volumeni)
            pricesi = fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', escenarios_test.index[i], 31).get(
                symbol)
            ini = pricesi['open'].iloc[0]
            sl = pricesi['open'].iloc[0] - df_decisiones['sl'].iloc[0] / 10000
            tp = pricesi['open'].iloc[0] + df_decisiones['tp'].iloc[0] / 10000

            for j in range(len(pricesi)):
                if pricesi['close'].iloc[j] == sl:
                    resultadoi = 'perdida'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif pricesi['close'].iloc[j] == tp:
                    resultadoi = 'ganada'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif j == len(pricesi) - 1:
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    if capitali <= 0:
                        resultadoi = 'perdida'
                    else:
                        resultadoi = 'ganada'
                    break

            resultado.append(resultadoi)
            capital.append(capitali)
            pips.append(pipsi)

        if escenarios_test['Escenario'].iloc[i] == 'B':
            operacioni = df_decisiones['operacion'].iloc[1]
            operacion.append(operacioni)
            volumeni = df_decisiones['volumen'].iloc[1]
            volumen.append(volumeni)
            pricesi = fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', escenarios_test.index[i], 31).get(
                symbol)
            ini = pricesi['open'].iloc[0]
            tp = pricesi['open'].iloc[0] - df_decisiones['tp'].iloc[1] / 10000
            sl = pricesi['open'].iloc[0] + df_decisiones['sl'].iloc[1] / 10000

            for j in range(len(pricesi)):
                if pricesi['close'].iloc[i] == sl:
                    resultadoi = 'perdida'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['open'].iloc[0] - pricesi['close'].iloc[j]) * 10000 * volumeni
                    break
                elif pricesi['close'].iloc[j] == tp:
                    resultadoi = 'ganada'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['open'].iloc[0] - pricesi['close'].iloc[j]) * 10000 * volumeni
                    break
                elif j == len(pricesi) - 1:
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['open'].iloc[0] - pricesi['close'].iloc[j]) * 10000 * volumeni
                    if capitali <= 0:
                        resultadoi = 'perdida'
                    else:
                        resultadoi = 'ganada'
                    break

            resultado.append(resultadoi)
            capital.append(capitali)
            pips.append(pipsi)

        if escenarios_test['Escenario'].iloc[i] == 'C':
            operacioni = df_decisiones['operacion'].iloc[2]
            operacion.append(operacioni)
            volumeni = df_decisiones['volumen'].iloc[2]
            volumen.append(volumeni)
            pricesi = fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', escenarios_test.index[i], 31).get(
                symbol)
            ini = pricesi['open'].iloc[0]
            sl = pricesi['open'].iloc[0] - df_decisiones['sl'].iloc[2] / 10000
            tp = pricesi['open'].iloc[0] + df_decisiones['tp'].iloc[2] / 10000

            for j in range(len(pricesi)):
                if pricesi['close'].iloc[j] == sl:
                    resultadoi = 'perdida'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif pricesi['close'].iloc[j] == tp:
                    resultadoi = 'ganada'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif j == len(pricesi) - 1:
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    if capitali <= 0:
                        resultadoi = 'perdida'
                    else:
                        resultadoi = 'ganada'
                    break

            resultado.append(resultadoi)
            capital.append(capitali)
            pips.append(pipsi)

        if escenarios_test['Escenario'].iloc[i] == 'D':
            operacioni = df_decisiones['operacion'].iloc[3]
            operacion.append(operacioni)
            volumeni = df_decisiones['volumen'].iloc[3]
            volumen.append(volumeni)
            pricesi = fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', escenarios_test.index[i], 31).get(
                symbol)
            ini = pricesi['open'].iloc[0]
            sl = pricesi['open'].iloc[0] - df_decisiones['sl'].iloc[3] / 10000
            tp = pricesi['open'].iloc[0] + df_decisiones['tp'].iloc[3] / 10000

            for j in range(len(pricesi)):
                if pricesi['close'].iloc[j] == sl:
                    resultadoi = 'perdida'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif pricesi['close'].iloc[j] == tp:
                    resultadoi = 'ganada'
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    break
                elif j == len(pricesi) - 1:
                    pipsi = abs((pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000)
                    capitali = (pricesi['close'].iloc[j] - pricesi['open'].iloc[0]) * 10000 * volumeni
                    if capitali <= 0:
                        resultadoi = 'perdida'
                    else:
                        resultadoi = 'ganada'
                    break

            resultado.append(resultadoi)
            capital.append(capitali)
            pips.append(pipsi)

    df_backtest['operacion'] = operacion
    df_backtest['volumen'] = volumen
    df_backtest['resultado'] = resultado
    df_backtest['pips'] = pips
    df_backtest['capital'] = capital
    df_backtest['capital_acm'] = df_backtest['capital'].cumsum() + 100000
    return df_backtest


df_backtest = backtest(df_decisiones)


def sharpe_neg(df_backtest):
    rf = 0.5
    rp = np.log(df_backtest['capital_acm'] / df_backtest['capital_acm'].shift()).dropna()
    rpm = rp.mean()
    sigma = rp.std()
    return - ((rpm - rf) / sigma)

operacion = ['compra', 'venta', 'compra', 'compra']

def sharpe_opt(x):
    sl = x[:4]
    tp = x[4:8]
    volumen = x[8:12]
    decisionesi = decisiones(operacion, sl, tp, volumen)
    backtesting = backtest(decisionesi)
    return sharpe_neg(backtesting)

min_bnd = np.array([3,3,1,1,8,8,3,3,100000,100000,50000,50000])

max_bnd = np.array([10,10,3,3,20,20,6,6,500000,500000,200000,200000])
bnds = (min_bnd, max_bnd)
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

optimization = ps.single.GlobalBestPSO(n_particles=24, dimensions=len(min_bnd), options=options,
                                       bounds=bnds)

cost, esc = optimization.optimize(sharpe_opt, iters=100)

sl = esc[:4]
tp = esc[4:8]
vol = esc[8:12]

df_desopt = decisiones(operacion, sl, tp, vol)
df_backtest_opt = backtest(df_desopt)

