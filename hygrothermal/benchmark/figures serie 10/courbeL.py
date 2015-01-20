# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 13:25:45 2014

@author: Rouchier
"""
import numpy as np
import pylab as P
import os
os.chdir('D:\MCF\Simulation\Python\inversion_benchmark\\figures serie 10')

YmYd = np.array([3.5478, 3.5478, 3.5480, 3.5510, 3.5660, 3.5801, 3.8616, 4.9999])
XmXp = np.array([0.1690, 0.1644, 0.1372, 0.0655, 0.0177, 0.0130, 0.0067, 0.0025])

Ysol = 3.5811
Xsol = 0.0209934

P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Tracés
P.hold(True)

P.plot(YmYd, XmXp, 'ko-', markersize = 6, linewidth = 1.5)
P.plot(Ysol, Xsol, marker = 'o', markersize = 10, markerfacecolor = 'r')
    
P.xlabel(r'$\| Y - Y_m \|^2$')
P.ylabel(r'$\| X - X_p \|^2$')


P.xlim((3.5, 5.1))
P.ylim((-0.01, 0.2))

fleche = dict(edgecolor='grey', facecolor='grey', shrink=0.03, width = 1, headwidth = 10)
flecherouge = dict(edgecolor='red', facecolor='red', shrink=0.03, width = 1, headwidth = 10)

P.annotate(r'$\alpha=0$',     xy=(YmYd[0], XmXp[0]), xytext = (4.2, 0.18), arrowprops=fleche)
P.annotate(r'$\alpha=0.001$', xy=(YmYd[1], XmXp[1]), xytext = (4.2, 0.16), arrowprops=fleche)
P.annotate(r'$\alpha=0.01$',  xy=(YmYd[2], XmXp[2]), xytext = (4.2, 0.14), arrowprops=fleche)
P.annotate(r'$\alpha=0.1$',   xy=(YmYd[3], XmXp[3]), xytext = (4.2, 0.12), arrowprops=fleche)
P.annotate(r'$\alpha=1$',     xy=(YmYd[4], XmXp[4]), xytext = (4.2, 0.08), arrowprops=fleche)
P.annotate('Solution',   xy=(Ysol, Xsol), xytext = (4.2, 0.10), arrowprops=flecherouge, color = 'red')
P.annotate(r'$\alpha=1$',     xy=(YmYd[4], XmXp[4]), xytext = (4.2, 0.08), arrowprops=fleche)
P.annotate(r'$\alpha=10$',    xy=(YmYd[5], XmXp[5]), xytext = (4.2, 0.06), arrowprops=fleche)
P.annotate(r'$\alpha=100$',   xy=(YmYd[6], XmXp[6]), xytext = (4.2, 0.04), arrowprops=fleche)
P.annotate(r'$\alpha=1000$',  xy=(YmYd[7], XmXp[7]), xytext = (4.2, 0.02), arrowprops=fleche)
           

fig1 = P.plt.gcf()
fig1.savefig('courbeL_benchmark.pdf', format='pdf', bbox_inches='tight')

