# -*- coding: utf-8 -*-
"""
Simple case
u, Te and xc are known
lambda_ and eps_ (the noise on Ti) are unknown, and given uniform priors
"""


from __future__ import division

from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import os
os.chdir('D:\\MCF\\Simulation\\Python\\Bayes\\Benchmark_thermique')

""" Discretisation et conditions aux limites """

# Space discretisation
size = 0.05
N_nodes = 21
delta_x = size / (N_nodes-1)
x = np.linspace(0, size, num=N_nodes)

# Time discretisation
time_step = 60.
time_stop = 8000
time_ = np.arange(0., time_stop+time_step, time_step)
N_samples = len(time_)

# Initial and boundary conditions
h_convec = 0
T_initial = 0
rho_cp  = 1.2e6

""" Vraies valeurs des variables d'entree """

xc_true     = 0.05 / 2
eps_T_true  = 0.5 # bruit sur la temperature
lambda_true = 0.3
# Input data : heat flow
data_direct = pd.read_csv('input_to_forward_problem.txt', delimiter='\t')
time_direct = data_direct['t (s)']
u_true = data_direct['U (W/m2)']
# Test data : measured temperature
data_inverse = pd.read_csv('input_to_inverse_problem.txt', delimiter='\t')
time_mesure = data_inverse['t (s)']
T_mesure = data_inverse['T(e/2)']
T_mesure += np.random.normal(0, eps_T_true, size=np.size(T_mesure))

""" Reseau bayesien """

import pymc as pm

# Prior sur lambda_
lambda_pm = pm.Uniform("conductivity", 0.1, 1) # la vraie valeur de lambda est 0.3
# Prior sur le bruit qu'on suppose inconnu
eps_T_pm = pm.Uniform('temperature noise', 0., 2.)
# Prior sur la position du capteur
xc_pm = pm.Normal('xc', 0.025, 1/0.003**2)

# Model
@pm.deterministic
def temperature(lambda_=lambda_pm, xc = xc_pm):
    
    a = lambda_ / rho_cp
    Biot = h_convec * delta_x / lambda_
    
    # Matrices A et b
    diag_moy = -2*np.ones(N_nodes)
    diag_sup = np.ones(N_nodes-1)
    diag_inf = np.ones(N_nodes-1)
    diag_moy[-1] += -2*Biot
    diag_sup[0]  += 1
    diag_inf[-1] += 1
    A = a / delta_x**2 * (np.diag(diag_moy)+np.diag(diag_inf, k=-1)+np.diag(diag_sup, k=1))
    b = np.zeros(N_nodes)
    b[0] += 2./(rho_cp * delta_x)
    
    # Calcul par résolution du système linéaire à chaque pas de temps
    T = T_initial * np.ones((N_samples, N_nodes))
    X = np.eye(N_nodes) - time_step * A
    for t in range(len(time_)-1):
        Y = T[t] + time_step*np.interp(time_[t+1], time_direct, u_true)*b
        T[t+1] = np.linalg.solve(X,Y)
    
    # Interpolation to get the temperature evolution at the sensor position
    #xc = np.min( (np.max((0, xc)),0.05) )
    foo = interp1d(x, T, bounds_error = False, fill_value = 0)
    T_xc = foo(xc)
    # Second interpolation to get this evolution at the time scale of measurements
    return np.interp(time_mesure, time_, T_xc)

# Likelihood
observation = pm.Normal("obs", mu = temperature, tau = 1./eps_T_pm**2, value=T_mesure, observed=True)

""" Inférence """

R = pm.MCMC([observation, lambda_pm, xc_pm, eps_T_pm])
R.sample(1000)
lambda_samples = R.trace('conductivity')[:]
xc_samples = R.trace('xc')[:]
eps_T_samples = R.trace('temperature noise')[:]

import pylab as plt

plt.subplot(3,1,1)
plt.hist(lambda_samples, bins=30)
plt.subplot(3,1,2)
plt.hist(xc_samples, bins=30)
plt.subplot(3,1,3)
plt.hist(eps_T_samples, bins=30)
