# -*- coding: utf-8 -*-
"""
Created on Wed May 07 11:21:37 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import numpy as np
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins')

# Esthétique

P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données

data_24h = pd.read_csv('serie8_pareto_24h.txt', delimiter='\t')
data_48h = pd.read_csv('serie8_pareto_48h.txt', delimiter='\t')
data_7j  = pd.read_csv('serie8_pareto_7j.txt',  delimiter='\t')

headers = ['R_T', 'R_HR', 'Erreur moyenne']

RT_1j, RHR_1j, Erreur_1j = [data_24h[_] for _ in headers]
RT_2j, RHR_2j, Erreur_2j = [data_48h[_] for _ in headers]
RT_7j, RHR_7j, Erreur_7j = [data_7j[_]  for _ in headers]


# Graphes

P.hold(True)

P.scatter(RT_1j, RHR_1j, s = 70, c = Erreur_1j*100, marker = 'o', cmap = 'RdYlGn_r', vmin = 0, vmax = 20)
P.scatter(RT_2j, RHR_2j, s = 70, c = Erreur_2j*100, marker = 's', cmap = 'RdYlGn_r', vmin = 0, vmax = 20)
P.scatter(RT_7j, RHR_7j, s = 70, c = Erreur_7j*100, marker = '^', cmap = 'RdYlGn_r', vmin = 0, vmax = 20)

P.plot(RT_1j, RHR_1j, 'k-')
P.plot(RT_2j, RHR_2j, 'k-')
P.plot(RT_7j, RHR_7j, 'k-')

P.colorbar()

P.xlim((1.014e-8, 1.036e-8))
P.ylim((3.1e-5, 3.7e-5))
P.xlabel(r'$R_T$')
P.ylabel(r'$R_H$')

P.text(x = 1.030e-8, y = 3.35e-5, s = '1 day', fontsize = 16)
P.text(x = 1.029e-8, y = 3.51e-5, s = '2 days', fontsize = 16)
P.text(x = 1.017e-8, y = 3.15e-5, s = '7 days', fontsize = 16)

ax = gca()
ax.yaxis.major.formatter.set_powerlimits((0,0))
ax.xaxis.set_label_coords(0.1, -0.1)

"""
fig = P.gcf()
fig.savefig('serie8_pareto_tous.pdf', format='pdf', bbox_inches='tight')
"""