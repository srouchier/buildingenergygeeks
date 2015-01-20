# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 09:44:56 2014

@author: Rouchier
"""
from copy import deepcopy
import numpy as np
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\Hygrobat\\resultats identification')
from hamopy import ham_library as ham

from hamopy.materials.standard import wood_fibre

WF_carac = wood_fibre
WF_prior = deepcopy(wood_fibre)
WF_bestf = deepcopy(wood_fibre)
WF_solut = deepcopy(wood_fibre)

# Isotherme de sorption du prior
WF_prior.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [22, 20, 62.5] })
# Isotherme de sorption de la solution sans régularisation
WF_bestf.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [-24.7, 5.68, 17.88] })
# Isotherme de sorption de la meilleure solution alpha = 100
WF_solut.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [21.22, 16.95, 17.14] })

HR = np.linspace(0.1, 0.9)
PC = ham.p_c(HR, T=293.15)

# Isothermes
W_carac = WF_carac.w(PC, T=293.15)
W_prior = WF_prior.w(PC, T=293.15)
W_bestf = WF_bestf.w(PC, T=293.15)
W_solut = WF_solut.w(PC, T=293.15)

# Esthétique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Tracés
P.hold(True)

a = [HR]*4
b = [W_carac, W_prior, W_bestf, W_solut]
colors = ['r-', 'k:', 'k--', 'k-']

for i in range(4):
    P.plot(a[i], b[i], colors[i], linewidth = 1.5)
    
P.xlabel(r'Relative humidity')
P.ylabel(r'Moisture content (kg/m$^3$)')
P.legend(('Measured', 'Prior', 'Best fit', 'Solution'), loc='upper left', ncol=2, fontsize=16)

P.xlim((0.1, 0.9))
#P.ylim((0, 40))


fig1 = P.plt.gcf()
fig1.savefig('isotherme.pdf', format='pdf', bbox_inches='tight')
