# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:18:31 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import os
from matplotlib.ticker import MultipleLocator
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins\serie4')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 16 })

# Lecture des données
data = pd.read_csv('serie4_precision.txt', delimiter='\t')
labels = data['Propriete']
N = len(labels)

resultat1 = data['1 capteur']
resultat2 = data['3 capteurs']

#Tracés
P.hold(True)

P.plot(range(N), resultat1, 'wo', markeredgecolor='k', markersize=10)
P.plot(range(N), resultat2, 'ws', markeredgecolor='k', markersize=10)

# Grille
P.plot([-1,N], [1, 1], 'r--', linewidth = 2)
P.grid(b=True, which='minor', axis = 'y', color='gray', linestyle='-', alpha = 0.5)

P.minorticks_on()
minorLocator   = MultipleLocator(0.1)
ax = P.gca()
ax.yaxis.set_minor_locator(minorLocator)

# Labels
P.xticks(range(N), (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_{mst}$', r'$\lambda_{tmp}$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18)
P.ylabel('Estimation / expectation ratio')
P.legend(('1 sensor', '3 sensors'), loc='upper left', fontsize=16)
P.xlim((-1, N))
P.ylim((0.8, 1.2))


fig1 = P.plt.gcf()
fig1.savefig('serie4_precision.pdf', format='pdf', bbox_inches='tight')
