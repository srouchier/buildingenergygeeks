import numpy as np

""" Unknown parameters and input data """

# True value of unknown parameters
xc_true       = 0.05 / 2  # sensor position
lambda_true   = 0.3       # thermal conductivity
sigma_T_true  = 0.2       # temperature noise
sigma_u_true  = 10        # heat flow noise

# Input data
import pandas

data_file = pandas.read_csv('inputs.txt', delimiter='\t')
time_file = data_file['t (s)']

u_file    = np.array( data_file['U (W/m2)'] )
u_file   += np.random.normal(0, sigma_u_true, size=np.size(u_file))
T_file    = np.array( data_file['T(e/2)'] )
T_file   += np.random.normal(0, sigma_T_true, size=np.size(T_file))

""" Setting up the Bayesian network """

import pymc as pm

# Priors on the unknowns
k_pm       = pm.Uniform("conductivity", 0.1, 1)
xs_pm      = pm.Normal('sensor position', 0.025, 1/0.001**2)
sigma_T_pm = pm.Exponential('temperature noise', 1.)
sigma_u_pm = pm.Uniform('heat flow noise', 0., 10.)

u_pm        = pm.Normal('real heat flow', mu = u_file, tau = 1./sigma_u_pm**2)

# Deterministic function to calculate the temperature
from simulate_temperature import T_func
@pm.deterministic
def T(k = k_pm, xs = xs_pm, u = u_pm):
    return T_func(k, xs, u, time_file)
    
# Likelihood
observation = pm.Normal("obs", mu = T, tau = 1./sigma_T_pm**2, value = T_file, observed=True)

""" Inference """

R = pm.MCMC([k_pm, xs_pm, sigma_T_pm, sigma_u_pm])

R.sample(10000, burn = 5000, thin = 5)

# Convergence diagnostics
pm.Matplot.plot(k_pm)

# Exporting the posteriors as numpy arrays
k_samples = R.trace('conductivity')[:]
sigma_T_samples = R.trace('temperature noise')[:]
sigma_u_samples = R.trace('heat flow noise')[:]
xc_samples = R.trace('sensor position')[:]
