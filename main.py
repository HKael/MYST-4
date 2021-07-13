
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import functions_PyMetatrader5 as fnmt5
import functions as fn
import visualizations as vs


#%%
# Archivo con el índice a usar
indice = pd.read_csv('files\\Unemployment Rate - United States.csv', index_col='DateTime')
# Eliminar columan de revised
indice.drop('Revised', axis=1, inplace=True)
# Convertir a datetime la columna de fechas
indice.index = pd.to_datetime(indice.index)

#%%
# Ejecutables
# local_exe = 'C:\\Program Files\\MetaTrader 5\\terminal64.exe'
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


