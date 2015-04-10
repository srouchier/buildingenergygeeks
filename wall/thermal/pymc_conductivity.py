

import numpy as np

""" Unknown parameters and input data """

# True value of unknown parameters
xc_true       = 0.05 / 2  # sensor position
lambda_true   = 0.3       # thermal conductivity
sigma_T_true  = 0.1       # temperature noise
sigma_u_true  = 4         # heat flow noise

# Input data
import pandas as pd
data_file = pd.read_csv('inputs.txt', delimiter='\t')
time_file = data_file['t (s)']
u_file    = np.array( data_file['U (W/m2)'] )
u_file   += np.random.normal(0, sigma_u_true, size=np.size(u_file))
T_file    = np.array( data_file['T(e/2)'] )
T_file   += np.random.normal(0, sigma_T_true, size=np.size(T_file))

""" Setting up the Bayesian network """

import pymc as pm

# Priors on the unknowns
lambda_pm = pm.Uniform("conductivity", 0.1, 1)
xc_pm     = pm.Normal('xc', 0.025, 1/0.001**2)
eps_T_pm  = pm.Exponential('temperature noise', 1.)
eps_u_pm  = pm.Uniform('flow noise', 0., 10.)

u_pm      = pm.Normal('real heat flow', mu = u_file, tau = 1./eps_u_pm**2)

# Deterministic function to calculate the temperature
from simulate_temperature import T_func
@pm.deterministic
def temperature(lambda_=lambda_pm, xc = xc_pm, u = u_pm):
    return T_func(lambda_, xc, u, time_file)
    
# Likelihood
observation = pm.Normal("obs", mu = temperature, tau = 1./eps_T_pm**2, value = T_file, observed=True)

""" Inference """

R = pm.MCMC([u_pm, lambda_pm, xc_pm, eps_T_pm, eps_u_pm, observation])
R.sample(10000, burn = 5000, thin = 5)

lambda_samples = R.trace('conductivity')[:]
eps_T_samples = R.trace('temperature noise')[:]
eps_u_samples = R.trace('flow noise')[:]
xc_samples = R.trace('xc')[:]
u_samples = R.trace('real heat flow')[:]

u_est = u_samples.mean(axis=0)

pm.Matplot.plot(R)
