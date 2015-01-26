import numpy as np
import pymc as pm
from copy import deepcopy


""" Reading measurements """

import pandas as pd
inputs = pd.read_csv('benchmark/benchmark_mesure_bruit.txt', delimiter = '\t')
t_mesure = inputs['t (s)']
# Boundary conditions
T_CL_obs  = np.array(inputs[['T (x=0)', 'T (x=10cm)']])
HR_CL_obs = np.array(inputs[['HR (x=0)', 'HR (x=10cm)']])
# Assemble
boundaries = [T_CL_obs, HR_CL_obs]

""" Priors """

# Noise priors
std_noise_T  = pm.Uniform("std_noise_T", 0, 0.5)
std_noise_HR = pm.Uniform("std_noise_HR", 0, 0.05)
std_noise_Q  = pm.Uniform("std_noise_Q", 0, 0.05)

# Adding the possibility of noise to boundary condition observations
# T_CL_sto  = pm.Normal("T_CL_sto",  mu = T_CL_obs,  tau = 1/std_noise_T**2 )
# HR_CL_sto = pm.Normal("HR_CL_sto", mu = HR_CL_obs, tau = 1/std_noise_HR**2)

# Parameter priors
lambda_0 = pm.Uniform("lambda_0", 0.02, 0.1)
lambda_m = pm.Uniform("lambda_m", 0.2, 1)
lambda_t = pm.Uniform("lambda_t", 5e-5, 2e-4)
cp       = pm.Uniform("cp", 500, 4000)
dp_p1    = pm.Uniform("dp_p1", 2.5e-11, 1e-10)
dp_p2    = pm.Uniform("dp_p2", 5e-11,   2e-10)
xi_p1    = pm.Uniform("xi_p1", 5, 35)
xi_p2    = pm.Uniform("xi_p2", 9, 40)
xi_p3    = pm.Uniform("xi_p3", 23, 95)
# Assemble
params = [lambda_0, lambda_m, lambda_t, cp, dp_p1, dp_p2, xi_p1, xi_p2, xi_p3]

""" Function """
from hamopy.algorithm import calcul
from hamopy.postpro import evolution, heat_flow
from benchmark.benchmark_input_7j_CLbruit import mesh, clim, init, time
mater_init = mesh.materials[0]

@pm.deterministic
def outputs(lambda_0_pm = lambda_0, lambda_m_pm = lambda_m, lambda_t_pm = lambda_t,
            cp_pm = cp, dp_p1_pm = dp_p1, dp_p2_pm = dp_p2,
            xi_p1_pm = xi_p1, xi_p2_pm = xi_p2, xi_p3_pm = xi_p3):
    
    # Material properties    
    m = deepcopy(mater_init)
    
    m.set_conduc(lambda_0_pm, lambda_m_pm, lambda_t_pm)
    m.set_capacity(cp_pm)
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [dp_p1_pm, dp_p2_pm]} )
                                   
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : [xi_p1_pm, xi_p2_pm, xi_p3_pm]  } )
    
    # Calcul
    resultat_simul = calcul(mesh, clim, init, time)
    
    # Post processing
    T_calcul  = evolution(resultat_simul, 'T',  x = 0.05, t = t_mesure)
    HR_calcul = evolution(resultat_simul, 'HR', x = 0.05, t = t_mesure)
    Q_calcul  = heat_flow(resultat_simul, mesh, clim, x = 0.05, t = t_mesure)
    
    return T_calcul, HR_calcul, Q_calcul
        

""" Likelihood """

T_wall_obs  = pm.Normal("T_wall_obs", mu = outputs[0], tau = 1/std_noise_T**2,
                        value = inputs['T (x=5cm)'], observed = True)
HR_wall_obs = pm.Normal("HR_wall_obs", mu = outputs[1], tau = 1/std_noise_HR**2,
                        value = inputs['HR (x=5cm)'], observed = True)
Q_wall_obs  = pm.Normal("Q_wall_obs", mu = outputs[2], tau = 1/std_noise_Q**2,
                        value = inputs['Q (x=5cm)'], observed = True)

""" Inference """


R = pm.MCMC([std_noise_T, std_noise_HR, std_noise_Q,
             lambda_0, lambda_m, lambda_t, cp, dp_p1, dp_p2, xi_p1, xi_p2, xi_p3,
             T_wall_obs, HR_wall_obs, Q_wall_obs])
R.sample(100)
lambda_0_samples = R.trace('lambda_0')[:]
lambda_m_samples = R.trace('lambda_m')[:]
lambda_t_samples = R.trace('lambda_t')[:]
cp_samples = R.trace('cp')[:]
dp_p1_samples = R.trace('dp_p1')[:]
dp_p2_samples = R.trace('dp_p2')[:]
xi_p1_samples = R.trace('xi_p1')[:]
xi_p2_samples = R.trace('xi_p2')[:]
xi_p3_samples = R.trace('xi_p3')[:]