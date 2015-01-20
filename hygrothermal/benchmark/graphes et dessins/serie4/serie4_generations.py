# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:18:31 2014

@author: Rouchier
"""
from __future__ import division
import pylab as P
import numpy as np
import pandas as pd
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins\serie4')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données
data = pd.read_csv('serie4_generations.txt', delimiter='\t')
gen, w_025, lambda_0, cp, dp_075 = \
    [data[_] for _ in ['Gen', 'w_025', 'lambda_0', 'cp', 'dp_075']]

#Tracés
P.hold(True)

couleurs = ['b-', 'g-', 'r-', 'c-']
p = ['w_025', 'lambda_0', 'cp', 'dp_075']

for i in range(len(p)):
    P.plot(gen, data[p[i]], couleurs[i], linewidth=2)

P.plot([0, 800], [1, 1], 'k--', linewidth=2)

P.xlabel('Generations')
P.ylabel('Estimation / expectation ratio')
P.legend((r'$w_{25}$', r'$\lambda_0$', r'$c_p$', r'$\delta_{p,75}$'), loc='upper right', fontsize=16)

#P.ylim((0, 3))


fig1 = P.plt.gcf()
fig1.savefig('serie4_generations.pdf', format='pdf', bbox_inches='tight')
