# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:18:31 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données
data = pd.read_csv('serie4_erreur.txt', delimiter='\t')
labels = data['Propriete']
N = len(labels)

resultat1 = data['1 capteur'] * 100
resultat2 = data['3 capteurs']* 100

#Tracés
P.hold(True)

P.plot(range(N), resultat1, 'wo', markeredgecolor='k', markersize=10)
P.plot(range(N), resultat2, 'ws', markeredgecolor='k', markersize=10)

#P.plot([-1,N], [1, 1], 'k--')
P.grid(b=True, which='major', axis = 'y', color='gray', linestyle='-')
P.xticks(range(N), (r'$c_p$',r'$\delta_{p,25}$',r'$\delta_{p,75}$',r'$\lambda_0$',
         r'$\lambda_m$', r'$\lambda_t$', r'$w_{25}$', r'$w_{50}$', r'$w_{75}$'), size=18)
P.ylabel(r'Identification error (\%)')
P.legend(('1 sensor', '3 sensors'), loc='upper left', fontsize=16)
P.xlim((-1, N))
P.ylim((0, 8))
"""
fig = P.plt.gcf()
fig.savefig('serie4_erreur.pdf', format='pdf', bbox_inches='tight')
"""