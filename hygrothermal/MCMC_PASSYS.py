

import numpy as np
import pymc as pm
from copy import deepcopy


""" Reading measurements """

import pandas as pd
inputs = pd.read_csv('passys/PASSYS_01.txt', delimiter = '\t')
t_mesure = inputs['temps (s)']
# Boundary conditions
T_CL_obs  = np.array(inputs[['T_0', 'T_16']]).T
HR_CL_obs = np.array(inputs[['HR_0', 'HR_16']]).T

""" Priors """

# Noise priors
std_noise_T  = 0.1
std_noise_HR = 0.01
std_noise_Q  = 0.01

# Adding the possibility of noise to boundary condition observations
T_CL  = pm.Normal('assumed temperature',  mu = T_CL_obs,  tau = 1./(std_noise_T**2), value = T_CL_obs)
HR_CL = pm.Normal('assumed RH', mu = HR_CL_obs, tau = 1./(std_noise_HR**2), value = HR_CL_obs)

# Parameter priors
lambda_0 = pm.Uniform("lambda_0", 0.02, 0.08, value = 0.038)  # expected value is 0.05
lambda_m = pm.Uniform("lambda_m", 0.1, 0.4, value = 0.192)      # expected value is 0.5
lambda_t = pm.Uniform("lambda_t", 5e-5, 2e-4, value = 1.08e-4) # expected value is 1e-4
cp       = pm.Uniform("cp", 500, 2000, value = 1103.1)        # expected value is 2000
dp_p1    = pm.Uniform("dp_p1", 2e-11, 7.5e-11, value = 3.75e-11)  # expected value is 5e-11
dp_p2    = pm.Uniform("dp_p2", 3e-11, 1.3e-10, value = 6.59e-11)  # expected value is 1e-10
xi_p1    = pm.Uniform("xi_p1", 9, 35, value = 17.704)           # expected value is 17
xi_p2    = pm.Uniform("xi_p2", 10, 40, value = 20.074)           # expected value is 19
xi_p3    = pm.Uniform("xi_p3", 23, 100, value = 49.816)          # expected value is 47

""" Function """
from hamopy import ham_library as ham
from hamopy.algorithm import calcul
#from hamopy.classes import Boundary
from hamopy.postpro import evolution, heat_flow
from passys.PASSYS import mesh, clim, init, time
mater_init = mesh.materials[0]
clim_init = clim

@pm.deterministic
def outputs(T_CL = T_CL, HR_CL = HR_CL,
            lambda_0 = lambda_0, lambda_m = lambda_m, lambda_t = lambda_t,
            cp = cp, dp_p1 = dp_p1, dp_p2 = dp_p2,
            xi_p1 = xi_p1, xi_p2 = xi_p2, xi_p3 = xi_p3):
    
    # Material properties    
    m = deepcopy(mater_init)
    c = deepcopy(clim_init)
    
    m.set_conduc(lambda_0, lambda_m, lambda_t)
    m.set_capacity(cp)
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [dp_p1, dp_p2]} )
                                   
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : [xi_p1, xi_p2, xi_p3]  } )
    
    mesh.replace_materials([m])
    
    for i in [0, 1]:
        c[i].data['T']    = T_CL[i]
        c[i].data['T_eq'] = T_CL[i]
        c[i].data['HR']   = HR_CL[i]
        c[i].data['p_v']  = HR_CL[i] * ham.p_sat(T_CL[i])
    
    # Calcul
    print('One evaluation\n')
    resultat_simul = calcul(mesh, c, init, time)
    
    if not type(resultat_simul)==dict:
        
        print('One of the simulations has failed \n')
        return np.zeros((7, len(t_mesure)))
        #return np.zeros(len(t_mesure))
        
    else:
        # Post processing
        T_calcul  = np.array([evolution(resultat_simul, 'T',  x = _, t = t_mesure) for _ in [0.04, 0.08, 0.12]])
        HR_calcul = np.array([evolution(resultat_simul, 'HR', x = _, t = t_mesure) for _ in [0.04, 0.08, 0.12]])
        Q_calcul  = heat_flow(resultat_simul, mesh, clim, x = 0.08, t = t_mesure)
        
        return np.row_stack((T_calcul, HR_calcul, Q_calcul))
        #return T_calcul
        

""" Likelihood """

valeurs = np.array(inputs[['T_4', 'T_8', 'T_12',
                           'HR_4', 'HR_8', 'HR_12', 'FLX_8']]).T

precision = np.array([1/std_noise_T**2, 1/std_noise_T**2, 1/std_noise_T**2,
                      1/std_noise_HR**2, 1/std_noise_HR**2, 1/std_noise_HR**2,
                      1/std_noise_Q**2])
taus = np.tile(precision, (len(t_mesure),1)).T

observation = pm.Normal('observation',
                        mu = outputs,
                        tau = taus,
                        value = valeurs,
                        observed = True)
"""
T_wall_obs  = pm.Normal("T_wall_obs", mu = outputs, tau = 1./0.1**2,
                        value = inputs['T (x=5cm)'], observed = True)
HR_wall_obs = pm.Normal("HR_wall_obs", mu = outputs[1], tau = 1./0.01**2,
                        value = inputs['HR (x=5cm)'], observed = True)
Q_wall_obs  = pm.Normal("Q_wall_obs", mu = outputs[2], tau = 1./0.01**2,
                        value = inputs['Q (x=5cm)'], observed = True)
"""

""" Inference """


R = pm.MCMC([observation, T_CL, HR_CL,
             lambda_0, lambda_m, lambda_t, cp, dp_p1, dp_p2, xi_p1, xi_p2, xi_p3 ])

R.sample(200)

lambda_0_samples = R.trace('lambda_0')[:]
lambda_m_samples = R.trace('lambda_m')[:]
lambda_t_samples = R.trace('lambda_t')[:]
cp_samples = R.trace('cp')[:]
dp_p1_samples = R.trace('dp_p1')[:]
dp_p2_samples = R.trace('dp_p2')[:]
xi_p1_samples = R.trace('xi_p1')[:]
xi_p2_samples = R.trace('xi_p2')[:]
xi_p3_samples = R.trace('xi_p3')[:]
#std_noise_T_samples  = R.trace('std of T noise')[:]
#std_noise_HR_samples = R.trace('std of HR noise')[:]
#std_noise_Q_samples  = R.trace('std of Q noise')[:]

pm.Matplot.plot(R)


np.savetxt('resultats_passys.txt',  np.array((lambda_0_samples, lambda_m_samples, lambda_t_samples,
                                 cp_samples, dp_p1_samples, dp_p2_samples,
                                 xi_p1_samples, xi_p2_samples, xi_p3_samples )).T)

"""
np.savetxt('foo.txt',  np.array((lambda_0_samples, lambda_m_samples, lambda_t_samples,
                                 cp_samples, dp_p1_samples, dp_p2_samples,
                                 xi_p1_samples, xi_p2_samples, xi_p3_samples)).T)
"""