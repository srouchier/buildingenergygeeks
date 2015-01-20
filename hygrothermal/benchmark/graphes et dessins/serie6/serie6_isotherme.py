# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:18:31 2014

@author: Rouchier
"""

import pylab as P
import numpy as np
import pandas as pd
import os
os.chdir('D:\MCF\Simulation\Python\inversion\graphes et dessins')

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 16 })

# Lecture des données
data = pd.read_csv('serie6_isotherme.txt', delimiter='\t')

HR = data['HR']
Wref = data['W ref']
W602 = data['W 602']
W605 = data['W 605']
W606 = data['W 606']
W609 = data['W 609']
N = len(Wref)

# Polynômes
p_ref, p_602, p_605, p_606, p_609 = \
    [np.polyfit(HR, _, 3) for _ in [Wref, W602, W605, W606, W609]]
dp_ref, dp_602, dp_605, dp_606, dp_609 = \
    [np.polyder(_) for _ in [p_ref, p_602, p_605, p_606, p_609]]

# Tracés étendus
HR_ext = np.linspace(0, 1)
Wref_ext, W602_ext, W605_ext, W606_ext, W_609_ext = \
    [np.polyval(_,HR_ext) for _ in [p_ref, p_602, p_605, p_606, p_609]]
CWref_ext, CW602_ext, CW605_ext, CW606_ext, CW_609_ext = \
    [np.polyval(_,HR_ext) for _ in [dp_ref, dp_602, dp_605, dp_606, dp_609]]
    
#Tracés
P.hold(True)

P.plot(HR_ext, Wref_ext, 'r--', linewidth=3)

marques = ['wo', 'ws', 'w^', 'wv']
i = 0
for W in [W602, W605, W606, W609]:
    P.plot(HR, W, marques[i], markeredgecolor='k', markersize=10)
    i += 1

for W in [W602_ext, W605_ext, W606_ext, W_609_ext]:
    P.plot(HR_ext, W, 'k-')

P.xlabel(r'Humidit\'e relative')
P.ylabel(r'w (kg/m$^3$)')
P.legend((r'R\'ef\'erence', '(1)', '(2)', '(3)', '(4)'), loc='upper left', fontsize=16)
P.xlim((0, 1))
P.ylim((-2, 40))


fig1 = P.plt.gcf()
fig1.savefig('serie6_isotherme.pdf', format='pdf')
