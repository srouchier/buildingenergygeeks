# -*- coding: utf-8 -*-
"""
Simple case
u, Te and xc are known
lambda_ and eps_ (the noise on Ti) are unknown, and given uniform priors
"""

from scipy.interpolate import interp1d
import numpy as np
import pandas as pd

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
eps_T_true  = 0.1 # bruit sur la temperature
# eps_u_true  = 50
lambda_true = 0.3
# Input data : heat flow
data_direct = pd.read_csv('input_to_forward_problem.txt', delimiter='\t')
time_direct = np.array( data_direct['t (s)'] )
u = data_direct['U (W/m2)']
# u += np.random.normal(0, eps_u_true, size=np.size(u))
# Test data : measured temperature
data_inverse = pd.read_csv('input_to_inverse_problem.txt', delimiter='\t')
time_mesure = np.array( data_inverse['t (s)'] )
T_mesure = data_inverse['T(e/2)']
T_mesure += np.random.normal(0, eps_T_true, size=np.size(T_mesure))

""" Parametrisation des fonctions d'entree """
# Choix du nombre de modes
N_modes = 20
t_modes = np.linspace(0, time_mesure[-1], N_modes)
# Fonctions f
def f_hat(t, j):
    
    delta_t = np.diff(t_modes).mean()
    
    f_rise = (t-t_modes[j-1]) / delta_t
    f_decr = 1 - (t-t_modes[j]) / delta_t
    
    if j == 0:
        is_rise = False
    else:
        is_rise = (t >= t_modes[j-1]) * (t <= t_modes[j])
        
    if j == len(t_modes)-1:
        is_decr = False
    else:
        is_decr = (t >= t_modes[j]) * (t <= t_modes[j+1])
    
    return f_rise * is_rise + f_decr * is_decr

""" Reseau bayesien """

import pymc as pm

# Prior sur le bruit qu'on suppose inconnu
eps_T_pm = pm.Uniform('noise', 0., 2.)
# Prior sur les parametres de u
um_pm = pm.Uniform('modes',0, 1500, size=N_modes-1)

# Model
lambda_ = lambda_true
xc      = xc_true
@pm.deterministic
def temperature(um = um_pm):
    
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
        # Calcul de u a partir de ses parametres
        f = np.array([f_hat(t+1, _) for _ in range(N_modes-1)])
        u = np.dot(um, f)
        Y = T[t] + time_step*u*b
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

R = pm.MCMC([observation, eps_T_pm, um_pm])
R.sample(1000)
eps_T_samples = R.trace('noise')[:]
um_samples = R.trace('modes')[:]

um_moyen= um_samples.mean(axis=0)
u_moyen = np.zeros_like(time_)
for t in range(len(time_)-1):
    f = np.array([f_hat(t+1, _) for _ in range(N_modes-1)])
    u_moyen[t] = np.dot(um_moyen, f)

import pylab as plt
plt.subplot(2,1,1)
plt.hist(eps_T_samples, bins=30)
plt.subplot(2,1,2)
plt.plot(time_, u_moyen)
