# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 13:25:45 2014

@author: Rouchier
"""
import numpy as np
import pylab as P

YmYd = np.array([13.881, 14.694, 15.723, 18.369, 21.498, 25.381, 30.999,
                 35.237, 39.690, 54.033, 70.296, 306.041])
XmXp = np.array([4.770, 2.623, 1.909, 1.084, 0.641, 0.363, 0.179, 0.118, 0.086,
                 0.044, 0.020, 0])

P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Tracés
P.hold(True)

P.plot(YmYd, XmXp, 'ko-', markersize = 6, linewidth = 1.5)
    
P.xlabel(r'$\| Y - Y_m \|^2$')
P.ylabel(r'$\| X - X_p \|^2$')

P.annotate(r'Best fit ($\alpha=0$)', xy=(YmYd[0], XmXp[0]), xytext = (100, 4),
           arrowprops=dict(facecolor='black', shrink=0.1, width = 1.5, headwidth = 10))
P.annotate(r'Solution ($\alpha=100$)', xy=(YmYd[7], XmXp[7]), xytext = (150, 3),
           arrowprops=dict(facecolor='black', shrink=0.02, width = 1.5, headwidth = 10))
P.annotate(r'Prior ($\alpha=+\infty$)', xy=(YmYd[-1], XmXp[-1]), xytext = (200, 2),
           arrowprops=dict(facecolor='black', shrink=0.1, width = 1))


#P.xlim((0.1, 0.9))
P.ylim((-0.2, 5))


fig1 = P.plt.gcf()
fig1.savefig('courbeL.pdf', format='pdf', bbox_inches='tight')

