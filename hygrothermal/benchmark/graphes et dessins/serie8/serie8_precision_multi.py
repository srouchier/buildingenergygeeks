# -*- coding: utf-8 -*-
"""
Created on Tue May 13 17:16:10 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import numpy as np
import os
from matplotlib.ticker import MultipleLocator
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins\serie8')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 16 })

# Lecture des données
data = pd.read_csv('serie8_precision_multi48h.txt', delimiter='\t')
N = len(data.keys())

# Tracé
bp = P.boxplot(data.values)
P.setp(bp['boxes'], color='black')
P.setp(bp['whiskers'], color='black')
P.setp(bp['fliers'], color='red', marker='+')

# Grille
P.plot([0, N+1], [1, 1], 'r--', linewidth = 2)
P.grid(b=True, which='minor', axis = 'y', color='gray', linestyle='-', alpha = 0.5)

P.minorticks_on()
minorLocator   = MultipleLocator(0.1)
ax = P.gca()
ax.yaxis.set_minor_locator(minorLocator)

# Labels
P.xticks(np.arange(N)+1, (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_m$', r'$\lambda_t$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18)
P.ylabel('Estimation / expectation ratio')

fig = P.plt.gcf()
fig.savefig('serie8_precision_multi2j.pdf', format='pdf', bbox_inches='tight')