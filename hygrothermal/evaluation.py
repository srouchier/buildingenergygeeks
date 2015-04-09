# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 13:39:19 2015

@author: simon
"""
import numpy as np
import pandas as pd

inputs = pd.read_csv('benchmark/benchmark_mesure_bruit.txt', delimiter = '\t')
t_mesure = inputs['t (s)']
# Boundary conditions
T_CL_obs  = np.array(inputs[['T (x=0)', 'T (x=10cm)']])
HR_CL_obs = np.array(inputs[['HR (x=0)', 'HR (x=10cm)']])

from copy import deepcopy

from hamopy.classes import Time
from hamopy.algorithm import calcul
from hamopy.postpro import evolution, heat_flow
from benchmark.benchmark_input_7j_CLbruit import mesh, init
mater_init = mesh.materials[0]

#meteo = np.array([t_mesure, T_CL_0_in, T_CL_1_in, HR_CL_0_in, HR_CL_1_in]).T
#np.savetxt('meteo.txt', meteo, delimiter = '\t', header = entete)
"""
clim1 = Boundary('Dirichlet',**{"file" : 'meteo.txt',
                                "time" : "# t (s)",
                                "T"    : "T (x=0)",
                                "HR"   : "HR (x=0)" })

clim2 = Boundary('Dirichlet',**{"file" : 'meteo.txt',
                                "time" : "# t (s)",
                                "T"    : "T (x=10cm)",
                                "HR"   : "HR (x=10cm)" })
"""

def evaluation(lambda_0, lambda_m, lambda_t, cp, dp_p1, dp_p2, xi_p1, xi_p2, xi_p3):
    
    # Material properties    
    m = deepcopy(mater_init)
    
    m.set_conduc(lambda_0, lambda_m, lambda_t)
    m.set_capacity(cp)
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [dp_p1, dp_p2]} )
                                   
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : [xi_p1, xi_p2, xi_p3]  } )
    
    mesh.replace_materials([m])
    
    # Calcul
    time = Time('variable',**{"delta_t"  : 3600,
                          "t_max"    : 7*24*3600,
                          "iter_max" : 12,
                          "delta_min": 1e-3,
                          "delta_max": 3600 } )
    resultat_simul = calcul(mesh, clim, init, time)
    
    # Post processing
    T_calcul  = evolution(resultat_simul, 'T',  x = 0.05, t = t_mesure)
    HR_calcul = evolution(resultat_simul, 'HR', x = 0.05, t = t_mesure)
    Q_calcul  = heat_flow(resultat_simul, mesh, clim, x = 0.05, t = t_mesure)
    
    return T_calcul, HR_calcul, Q_calcul

T_mesure  = inputs['T (x=5cm)']
HR_mesure = inputs['HR (x=5cm)']
Q_mesure  = inputs['Q (x=5cm)']

burn = 0
T, HR, Q = evaluation(lambda_0_samples[burn:].mean(),
                      lambda_m_samples[burn:].mean(),
                      lambda_t_samples[burn:].mean(),
                      cp_samples[burn:].mean(),
                      dp_p1_samples[burn:].mean(),
                      dp_p2_samples[burn:].mean(),
                      xi_p1_samples[burn:].mean(),
                      xi_p2_samples[burn:].mean(),
                      xi_p3_samples[burn:].mean())


T2, HR2, Q2 = evaluation(0.05, 0.5, 1e-4, 2000, 5e-11, 1e-10, 17, 19, 47)
blu = evaluation(0.05, 0.5, 1e-4, 2000, 5e-11, 1e-10, 17, 19, 47)

foo = np.sum((T_mesure-T)**2)
bar = np.sum((T_mesure-T2)**2)
