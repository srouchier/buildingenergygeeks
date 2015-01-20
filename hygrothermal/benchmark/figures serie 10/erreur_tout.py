# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 15:40:22 2014

@author: Rouchier
"""

import numpy as np
import pandas as pd
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\inversion_benchmark\\figures serie 10')
data = pd.read_csv('erreurs.txt', delimiter='\t')

prior = [0.125, 0.2, 0.2, 0.25, 0.25, 0.25, 0.176, 0.289, 0.255, 0.222]
alpha = data['alpha']
labels = ['cp', 'lambda_0', 'lambda_m', 'lambda_t', 'dp_p1', 'dp_p2', 'xi_p1', 'xi_p2', 'xi_p3', 'moyenne']
marques = ['ko-', 'kv-', 'kv-', 'kv-', 'ks-', 'ks-', 'k^-', 'k^-', 'k^-', 'ro-']
marques2 = ['ko--', 'kv--', 'kv--', 'kv--', 'ks--', 'ks--', 'k^--', 'k^--', 'k^--', 'ro--']
couleur = ['black', 'white', 'grey', 'black', 'white', 'black', 'white', 'grey', 'black', 'red']

P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Tracés
P.hold(True)

N = len(labels)
for i in range(N):
    P.plot(range(8), data[labels[i]]*100, marques[i], markersize = 8, linewidth = 1.5, markerfacecolor = couleur[i])
for i in range(N):
    P.plot([7, 8], [data[labels[i]][7]*100,prior[i]*100], marques2[i], markersize = 8, linewidth = 1, markerfacecolor = couleur[i])


"""
P.semilogx(alpha, [Yprior]*7, 'r--', linewidth=1.5)
"""
P.xlabel(r'Regularisation parameter $\alpha$')
P.ylabel(r'Estimation error $\mathbf{e_\alpha}$ ($\%$)')

P.xticks(range(9), (r'$0$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^0$',
         r'$10^1$',r'$10^2$',r'$10^3$','Prior'), size=18)

#P.grid(b=None, which='major', axis='y')
P.xlim((-0.5, 8.5))
P.ylim((0, 60))
P.legend((r'$c_p$',r'$k_0$',r'$k_m$', r'$k_t$',r'$\delta_{p,25}$',
          r'$\delta_{p,75}$', r'$\xi_{25}$', r'$\xi_{50}$',
          r'$\xi_{75}$', 'avg.'),loc='upper right', ncol=4,
          labelspacing=0.2, columnspacing=0.8, handletextpad=0.4, fontsize=16)

fig1 = P.plt.gcf()
fig1.savefig('erreur_identification_tout.pdf', format='pdf', bbox_inches='tight')
