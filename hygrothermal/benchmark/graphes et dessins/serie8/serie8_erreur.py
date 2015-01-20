# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:18:31 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins\serie8')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données
data = pd.read_csv('serie8_erreur_multi.txt', delimiter='\t')
labels = data['Propriete']
N = len(labels)

error_1day = data['24h'] * 100
error_2day = data['48h'] * 100
error_7day = data['7j'] * 100

#Tracés
P.hold(True)

P.plot(range(N), error_1day, 'wo', markeredgecolor='k', markersize=10)
P.plot(range(N), error_2day, 'ws', markeredgecolor='k', markersize=10)
P.plot(range(N), error_7day, 'w^', markeredgecolor='k', markersize=10)

#P.plot([-1,N], [1, 1], 'k--')
P.grid(b=True, which='major', axis = 'y', color='gray', linestyle='-')
P.xticks(range(N), (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_m$', r'$\lambda_t$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18)
P.ylabel(r'Identification error (\%)')
P.legend(('1 day', '2 days', '7 days'), loc='upper right', fontsize=16)
P.xlim((-1, N))
P.ylim((0, 7))

fig = P.plt.gcf()
fig.savefig('serie8_erreur_multi.pdf', format='pdf', bbox_inches='tight')
