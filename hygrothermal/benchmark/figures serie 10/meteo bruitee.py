# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 14:34:24 2014

@author: Rouchier
"""
from __future__ import division
import pandas as pd
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\inversion_benchmark\\figures serie 10')

data0 = pd.read_csv('benchmark_mesure_bruit.txt', delimiter='\t')

t = data0['t (s)'] / 3600 / 24
T_ext = data0['T (x=0)'] - 273.15
T_int = data0['T (x=10cm)'] - 273.15
HR_ext = data0['HR (x=0)'] * 100
HR_int = data0['HR (x=10cm)'] * 100

# Tracés
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })
P.hold(True)

a = [t]*2
b = [T_ext, T_int]
colors = ['black', 'grey']

for i in range(2):
    P.plot(a[i], b[i], colors[i], linewidth = 1.5)
    
P.xlabel('Time (days)')
P.ylabel(r'Temperature ($^\circ$C)')

P.xlim((0, 7))
#P.ylim((-0.2, 5))

P.legend(('Exterior', 'Interior'), loc='lower right', ncol=2, fontsize=16)

fig1 = P.plt.gcf()
fig1.savefig('meteo_temperature.pdf', format='pdf', bbox_inches='tight')

