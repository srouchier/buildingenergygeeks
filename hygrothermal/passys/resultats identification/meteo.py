# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 14:34:24 2014

@author: Rouchier
"""
from __future__ import division
import pandas as pd
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\Hygrobat\\resultats identification')

data0 = pd.read_csv('PASSYS_01.txt', delimiter='\t')

t = data0['temps (s)'] / 3600 / 24
T_ext = data0['T_16'] - 273.15
T_int = data0['T_0'] - 273.15
HR_ext = data0['HR_16'] * 100
HR_int = data0['HR_0'] * 100

# Tracés
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })
P.hold(True)

a = [t]*5
b = [HR_ext, data0['HR_12']*100, data0['HR_8']*100, data0['HR_4']*100, HR_int]
colors = ['0.', '0.2', '0.4', '0.6', '0.8']

for i in range(5):
    P.plot(a[i], b[i], colors[i], linewidth = 1.5)
    
P.xlabel('Time (days)')
P.ylabel(r'Relative humidity ($\%$)')

P.xlim((0, 14))
#P.ylim((-0.2, 5))

P.legend(('Exterior', 'Interior'), loc='upper left', ncol=2, fontsize=16)
"""
fig1 = P.plt.gcf()
fig1.savefig('meteo_humidite.pdf', format='pdf', bbox_inches='tight')
"""
