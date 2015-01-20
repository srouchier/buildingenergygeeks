# -*- coding: utf-8 -*-
"""
Created on Wed May 07 11:21:37 2014

@author: Rouchier
"""

import pylab as P
import pandas as pd
import numpy as np
import os
os.chdir('D:\MCF\Simulation\Python\inversion_benchmark\graphes et dessins\serie8')

# Esthétique

P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Lecture des données

data  = pd.read_csv('serie8_pareto_7j.txt',  delimiter='\t')
RT, RHR, Erreur = [data[_]  for _ in ['R_T', 'R_HR', 'Erreur moyenne']]

RTref = 1.0161730935117E-08
RHRref = 0.0000314095519543936

# Graphes

P.hold(True)

P.scatter(RT, RHR, s = 70, c = Erreur*100, marker = '^', cmap = 'RdYlGn_r', vmin = 0, vmax = 20)
P.plot(RT, RHR, 'k-')
P.plot(RTref, RHRref, 'k^', markersize = 10, markerfacecolor = 'w', markeredgewidth = 2)

"""
# Isoler le meilleur individu d'un front de Pareto
tuple_ = np.where(Erreur == min(Erreur))
i = tuple_[0][0]
RTopt  = RT[i]
RHRopt = RHR[i]
P.annotate('best', xy=(RTopt, RHRopt), xytext = (1.0159e-8, 3.146e-5),
           arrowprops=dict(facecolor='black', shrink=0.05, width = 2))
"""

title('7 days')

P.colorbar()

P.xlim((1.0158e-8, 1.0162e-8))
P.ylim((3.14e-5, 3.15e-5))
P.xlabel(r'$R_T$')
P.ylabel(r'$R_H$')

ax = gca()
ax.yaxis.major.formatter.set_powerlimits((0,0))
ax.xaxis.set_label_coords(0.1, -0.1)

"""
fig = P.gcf()
fig.savefig('serie8_pareto_7jours.pdf', format='pdf', bbox_inches='tight')
"""