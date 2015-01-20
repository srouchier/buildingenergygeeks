# -*- coding: utf-8 -*-
"""
Created on Fri May 09 16:28:52 2014

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

Erreur_1j = data_24h['Erreur moyenne']*100
Erreur_2j = data_48h['Erreur moyenne']*100
Erreur_7j = data_7j['Erreur moyenne']*100

bp = P.boxplot([Erreur_1j, Erreur_2j, Erreur_7j])
P.setp(bp['boxes'], color='black')
P.setp(bp['whiskers'], color='black')
P.setp(bp['fliers'], color='red', marker='+')

P.xticks(np.arange(3)+1, ('1 day', '2 days', '7 days'), size=18)
P.ylabel(r'Avg. identification error (\%)')

fig = P.gcf()
fig.savefig('serie8_moustache.pdf', format='pdf', bbox_inches='tight')