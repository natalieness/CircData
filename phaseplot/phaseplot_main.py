'''

Script that takes an excel or csv file with phase data, plots a circular scatter plot
and caculates some circular statistics for each sample

'''
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from cmath import rect, phase 

import tkinter as tk
from tkinter import filedialog
from setup import save_generic_pandas_df, variance_angle, get_mean_angle, hour2rad, rad2hour, get_file, plot_circ_scatter

#ask for file to import 
df = get_file(type='xlsx')
#assumes data is organised in columns. If not, transpose first

circ_data = pd.DataFrame(columns=['name', 'Rayleigh Z', 'Rayleigh p', 'mean phase', 'vector length','N'])

#iterate through columns
for c in range(df.shape[1]):
    data = df.iloc[:,c]
    data = data.dropna() #remove NaNs
    name = df.columns[c][:-4] #gets name without extension

    #Rayleigh test on data
    #convert phases to radians for Rayleigh test
    data_rad = np.array(list(map(hour2rad, data)))
    (p_i,z_i) = pc.tests.rayleigh(data_rad)

    print('For sample %s, Rayleigh test p = %.10f'%(name, p_i))

    ### Plot circular plot of phases
    fig, V, mean_T = plot_circ_scatter(data_rad, name, color='gray')

    N = len(data_rad) #get number of cells
    print('For sample %s with %i cells, mean angle = %.2f, vector length = %.2f'%(name, N, rad2hour(mean_T), V))

    #append to circ data 
    circ_data.loc[c] = [name, z_i, p_i, rad2hour(mean_T), V, N]

#save circ data 
save_generic_pandas_df(circ_data, 'circ_data')
