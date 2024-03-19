'''

Data handling and plotting functions for circular data

'''

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from cmath import rect, phase 

import tkinter as tk
from tkinter import filedialog


def save_generic_pandas_df(df, filename):
    filepath = '%s.xlsx'%filename
    df.to_excel(filepath, index=False)    
    
    
def variance_angle(rad):
    """
    rad: angles in radians 
    """
    S = np.array(rad)
    C = np.array(rad)

    length = C.size

    S = np.sum(np.sin(S))
    C = np.sum(np.cos(C))
    R = np.sqrt(S**2 + C**2)
    R_avg = R/length
    V = 1- R_avg

    return V   

def get_mean_angle(rad):
    #deg is a list of angles in degrees 
    a = (phase(sum(rect(1, r) for r in rad)/len(rad)))
    if a < 0: 
        a = 2*np.pi+a 
    return a

def hour2rad(h):
    #h is a float between 0 and 24
    return 2* np.pi*h/24

def rad2hour(r):
    #r is a float between 0 and 2pi
    return r/(2*np.pi)*24

def get_file(type='xlsx'):
    #ask for file to import 
    #create root window 
    root = tk.Tk()
    root.withdraw() #suppresses GUI
    file_path = filedialog.askopenfilename(title='Open the file to import') #prompts to select file 
    if type == 'xlsx':
        df= pd.read_excel(file_path)
    elif type == 'csv':
        df= pd.read_csv(file_path)
    else:
        print('File type not recognised')

    return df



def plot_circ_scatter(data_rad, name, color='gray'):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # set theta values to range from 0 to 2*pi
    theta = np.linspace(0, 2*np.pi, 24, endpoint=False)

    # set radial values to 1 for all theta values
    r = 0.99

    # plot points on the inside of the plot, with small offset
    pos = [] 
    plotted = []
    dist = 0.02
    for j in data_rad:
        m_list = [1 for i in plotted if abs(i-j) < dist]
        sum_p= sum(m_list)
        ax.plot(j, r-(0.02*sum_p), 'o', color='gray', markersize=2)
        plotted.append(j)
        pos.append(sum_p)

    ax.set_ylim(0, 1)

    # set theta ticks to clock positions
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    hour_labels = ['0',  '6', '12','18']
    ax.set_xticks([0,np.pi/2, np.pi, 1.5*np.pi], hour_labels, fontsize=25)

    #set y ticks to nothing
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.grid(False)
    ax.tick_params(pad=12)


    #plot mean angle vector 
    V = 1-variance_angle(data_rad)
    mean_T = get_mean_angle(data_rad)
    #ax.arrow(0,0,0.5,0.5, scale=1, width=0.02)

    X_comp = 1 * np.sin(mean_T)
    Y_comp = 1 * np.cos(mean_T) #radius = 1

    ax.quiver(0,0,X_comp,Y_comp,  scale=2/V , width=0.016, headwidth=3.5, headlength=3, headaxislength=3, color='black', edgecolor='black',linewidth=0.7,zorder=10)

    #plot central circle 
    ax.scatter(0,0,marker='o', color='black')
    ax.set_title(name, fontsize=25, pad=10)

    return fig, V, mean_T


