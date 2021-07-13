
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
#%%
import pandas as pd


unenrate = pd.read_csv('files\\Unemployment Rate - United States.csv')
unenrate['DateTime'] = pd.to_datetime(unenrate['DateTime'])
unenrate = unenrate[['DateTime','Actual','Consensus','Previous']]
unenrate = unenrate.set_index('DateTime')




# %%
