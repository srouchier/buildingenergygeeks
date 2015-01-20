# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:38:13 2014

@author: Rouchier
"""

import pylab as P
import numpy as np
import pandas as pd
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 16 })

# Données
data = pd.read_csv('serie4_sensibilite_HR.txt', delimiter='\t')
labels = data['Parameter']
N = len(labels)
S       = data['First_Order']
S_err   = data['First_Order_Conf']
ST      = data['Total_Order']
ST_err  = data['Total_Order_Conf']

ind = np.arange(N)
width = 0.35

fig, ax = P.subplots()

rects1 = ax.bar(ind, S, width, color='0.7', yerr=S_err)
rects2 = ax.bar(ind+width, ST, width, color='0.3', yerr=ST_err)

ax.set_xticks(ind+width)
ax.set_xticklabels( (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_{mst}$', r'$\lambda_{tmp}$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18 )
ax.set_ylim((-0.05,0.6))

ax.legend( (rects1[0], rects2[0]), (r'$S$', r'$S_T$'), loc='upper left' )
#P.title(r'$R_{HR}$')

fig.savefig('serie4_sensibilite_HR.pdf', format='pdf')