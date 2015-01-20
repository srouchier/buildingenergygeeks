# -*- coding: utf-8 -*-
"""
Created on Tue May 13 16:31:12 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import os
from matplotlib.ticker import MultipleLocator
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins\serie8')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 16 })

# Lecture des données
data = pd.read_csv('serie8_precision_mono1.txt', delimiter='\t')
labels = data['Propriete']
N = len(labels)

data_1day = data['24h'] / data['Objectif']
data_2day = data['48h'] / data['Objectif']
data_7day = data['7j']  / data['Objectif']

# Tracés
P.hold(True)

P.plot(range(N), data_1day, 'wo', markeredgecolor='k', markersize=10)
P.plot(range(N), data_2day, 'ws', markeredgecolor='k', markersize=10)
P.plot(range(N), data_7day, 'w^', markeredgecolor='k', markersize=10)

# Grille
P.plot([-1,N], [1, 1], 'r--', linewidth = 2)
P.grid(b=True, which='minor', axis = 'y', color='gray', linestyle='-', alpha = 0.5)

P.minorticks_on()
minorLocator   = MultipleLocator(0.1)
ax = P.gca()
ax.yaxis.set_minor_locator(minorLocator)

# Labels
P.xticks(range(N), (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_m$', r'$\lambda_t$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18)
P.ylabel('Estimation / expectation ratio')
P.legend(('1 day', '2 days', '7 days'), loc='lower left', fontsize=16)

# Fenetre
P.xlim((-1, N))
P.ylim((0, 2))


fig = P.plt.gcf()
fig.savefig('serie8_precision_mono1.pdf', format='pdf', bbox_inches='tight')
