# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 15:40:22 2014

@author: Rouchier
"""

import numpy as np
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\inversion_benchmark\\figures serie 10')

alpha = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])

erreur = np.array([35.8, 31.2, 17.9, 4.8, 8.5, 12.5, 18.0])
Yprior = 22.2



P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Tracés
P.hold(True)

P.semilogx(alpha, erreur, 'ko-', markersize = 6, linewidth = 1.5)

P.semilogx(alpha, [Yprior]*7, 'r--', linewidth=1.5)
P.text(100, Yprior+1, 'Prior', fontdict=dict(color='red'))
    
P.xlabel(r'Regularisation parameter $\alpha$')
P.ylabel(r'Avg. estimation error $\mathbf{e_\alpha}$ ($\%$)')

P.grid(b=None, which='major', axis='y')
#P.xlim((3.5, 5.1))
#P.ylim((-0.01, 0.2))
P.legend(('Average', 'Prior', 'Best fit', 'Solution'), loc='upper left', ncol=2, fontsize=14)
"""
fig1 = P.plt.gcf()
fig1.savefig('erreur_identification.pdf', format='pdf', bbox_inches='tight')
"""