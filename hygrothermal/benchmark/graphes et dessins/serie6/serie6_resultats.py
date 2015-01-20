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
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données
data = pd.read_csv('serie6_reconstruction.txt', delimiter='\t')
temps = data['t (s)']
temps_j = temps/(24*3600)
mesures = data['Mesures']*100
reconstruction = data['Reconstruction']*100

#Tracés
P.hold(True)

P.plot(temps_j, mesures, 'r--', linewidth=2)
P.plot(temps_j, reconstruction, 'k-')

P.xlabel('Temps (jours)')
P.ylabel(r'Humidit\'e relative ($\%$)')
P.legend(('Mesure', 'Reconstruction'), loc='lower right', fontsize=16)

#P.ylim((0, 3))


fig1 = P.plt.gcf()
fig1.savefig('serie6_reconstruction.pdf', format='pdf')
