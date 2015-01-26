from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import os
os.chdir('/home/simon/Simulation/InverseBuilding/thermal')

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

lambda_true = 0.3
xc_true     = 0.05 / 2
eps_T_true  = 0.2
eps_u_true  = 10

""" Reading measurements """
inputs = pd.read_csv('inputs.txt', delimiter='\t')
time_mesure = inputs['t (s)']
# Surface heat flow
u_mesure  = np.array( inputs['U (W/m2)'] )
u_mesure += np.random.normal(0, eps_u_true, size=np.size(u_mesure))
# Sensor temperature
T_mesure  = np.array( inputs['T(e/2)'] )
T_mesure += np.random.normal(0, eps_T_true, size=np.size(T_mesure))

""" Reseau bayesien """

import pymc as pm

# Prior sur lambda_
lambda_pm = pm.Uniform("conductivity", 0.1, 1) # la vraie valeur de lambda est 0.3
# Prior sur le bruit qu'on suppose inconnu
eps_T_pm = pm.Uniform('temperature noise', 0., 2.)
# Prior sur la position du capteur
xc_pm = pm.Normal('xc', 0.025, 1/0.003**2)
# Prior sur le bruit du flux
eps_u_pm = pm.Uniform('flow noise', 0., 30.)
# Estimated real heat flow
u_pm = pm.Normal('real heat flow', mu = u_mesure, tau = 1./eps_u_pm**2)

# Model
@pm.deterministic
def temperature(lambda_=lambda_pm, xc = xc_pm, u = u_pm):
    
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
        Y = T[t] + time_step*np.interp(time_[t+1], time_mesure, u)*b
        T[t+1] = np.linalg.solve(X,Y)
    
    # Interpolation to get the temperature evolution at the sensor position
    #xc = np.min( (np.max((0, xc)),0.05) )
    foo = interp1d(x, T, bounds_error = False, fill_value = 0)
    T_xc = foo(xc)
    # Second interpolation to get this evolution at the time scale of measurements
    return np.interp(time_mesure, time_, T_xc)

# Likelihood
observation = pm.Normal("obs", mu = temperature, tau = 1./eps_T_pm**2, value = T_mesure, observed=True)

# Observed heat flow
#u_est = pm.Uniform('estimated flow', 0, 1500, size = np.size(u_mesure))
#u_obs = pm.Normal('heat_flow_obs', mu = u_est, tau = 1./eps_u_pm**2, value = u_mesure, observed = True)

""" Inférence """

R = pm.MCMC([observation, lambda_pm, xc_pm, eps_T_pm, eps_u_pm, u_pm])
R.sample(10000)
lambda_samples = R.trace('conductivity')[:]
eps_T_samples = R.trace('temperature noise')[:]
eps_u_samples = R.trace('flow noise')[:]
xc_samples = R.trace('xc')[:]
u_samples = R.trace('real heat flow')[:]

u_est = u_samples.mean(axis=0)

import pylab as plt

plt.subplot(3,1,1)
plt.hist(lambda_samples, bins=30)
plt.subplot(3,1,2)
plt.hist(xc_samples, bins=30)
plt.subplot(3,1,3)
plt.hist(eps_T_samples, bins=30)

plt.boxplot((lambda_samples / lambda_true,
             xc_samples / xc_true,
             eps_T_samples / eps_T_true,
             eps_u_samples / eps_u_true))