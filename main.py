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
import functions_PyMetatrader5 as fnmt5
import functions as fn
import visualizations as vs

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
indice_prueba = indice.iloc[0:13,:]
indice_train = indice.iloc[13:26,:]

escenarios_prueba = df_escenarios.iloc[0:13,:]
escenarios_test = df_escenarios.iloc[13:26,:]

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

df_decisiones = pd.DataFrame(columns=['escenario', 'operacion', 'sl', 'tp', 'volumen'], index=[0,1,2,3])
df_decisiones.iloc[0] = ['A'] + escenarioa
df_decisiones.iloc[1] = ['B'] + escenariob
df_decisiones.iloc[2] = ['C'] + escenarioc
df_decisiones.iloc[3] = ['D'] + escenariod

df_backtest = pd.DataFrame(columns = ['escenario', 'operacion', 'volumen', 'resultado', 'pips',
                                      'capital', 'capital_acm'], index = escenarios_test.index)

df_backtest['escenario'] = escenarios_test['Escenario']

for i in range(len(escenarios_test)):
    operacion = []
    volumen = []
    resultado = []
    pips = []
    capital = []
    capita_acm = []
    if escenarios_test['Escenario'].iloc[i] == 'A':
        operacioni = df_decisiones['operacion'].iloc[0]
        operacion.append(operacioni)
        volumeni = df_decisiones['volumen'].iloc[0]
        volumen.append(volumeni)
        pricesi = fnmt5.f_hist_prices_from(mt5_client, [symbol], 'M1', escenarios_test.index[i], 31).get(symbol)
        ini = pricesi['open'].iloc[0]
        sl = pricesi['open'].iloc[0] - df_decisiones['sl'].iloc[0]/10000
        tp = pricesi['open'].iloc[0] + df_decisiones['tp'].iloc[0]/10000

        for i in i in pricesi['close']:
            if i == sl:
                resultadoi = 'perdida'
                pipsi = (pricesi['open'].iloc[0] - pricesi) * 10000
                capitali = pipsi*volumeni






