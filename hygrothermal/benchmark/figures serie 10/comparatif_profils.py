# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 10:54:35 2014

@author: Rouchier
"""
from __future__ import division
import pylab as P
import numpy as np
import pandas as pd
import os
os.chdir('D:\\MCF\\Simulation\\Python\\inversion_benchmark\\figures serie 10')

data_mesure = pd.read_csv('benchmark_mesure_bruit.txt', delimiter='\t')
data_prior = pd.read_csv('a infini - prior.txt', delimiter='\t')
data_bestfit = pd.read_csv('a0 - best fit.txt', delimiter='\t')
data_solution = pd.read_csv('a1 - solution.txt', delimiter='\t')

# Lecture des données
colonne = 'T (x=5cm)'
temps = data_mesure['t (s)'] / 24 / 3600
Mesure   = data_mesure[colonne]
Prior    = data_prior[colonne]
Bestfit  = data_bestfit[colonne]
Solution = data_solution[colonne]
# Mesure = np.reshape( np.column_stack((data_mesure[_] for _ in ['T_4', 'T_8', 'T_12'])) ,(12096,))

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

P.hold(True)

a = [temps]*4
b = [Mesure, Prior, Bestfit, Solution]
colors = ['r-', 'k:', 'k--', 'k-']

for i in range(4):
    P.plot(a[i], b[i], colors[i], linewidth = 1.5)

P.xlabel('Time (days)')
P.ylabel(r'Heat flux (W/m$^2$)')
P.legend(('Measured', 'Prior', 'Best fit', 'Solution'), loc='upper left', ncol=2, fontsize=14)

P.xlim((0, 7))
#P.ylim((0, 9))

"""
fig1 = P.plt.gcf()
fig1.savefig('FLX_16.pdf', format='pdf', bbox_inches='tight')
"""