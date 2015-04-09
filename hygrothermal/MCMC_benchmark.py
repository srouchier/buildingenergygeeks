from __future__ import division

import numpy as np
import pymc as pm
from copy import deepcopy
from scipy.signal import resample

""" Reading measurements """
# Loading text data
import pandas
datafile = pandas.read_csv('benchmark/benchmark_mesure_bruit.txt', delimiter = '\t')
time_mesure = datafile['t (s)']
# Resampling
time_step_old = time_mesure[1] - time_mesure[0]    # original time step of the data file
time_step_new = 1*3600                             # time step of the resampling
num = np.floor(len(datafile) * time_step_old / time_step_new)  # number of points in the new sample
# Input boundary conditions
T_CL_file  = np.array(datafile[['T (x=0)', 'T (x=10cm)']]).T
HR_CL_file = np.array(datafile[['HR (x=0)', 'HR (x=10cm)']]).T
# Input boundary conditions with downsampling
(T_CL_down, time_new) = resample(T_CL_file, num, time_mesure, axis=1)
HR_CL_down = resample(HR_CL_file, num, axis=1)
# Output sensor measurements
outputs_file = np.array(datafile[['T (x=5cm)', 'HR (x=5cm)', 'Q (x=5cm)']]).T
outputs_down = resample(outputs_file, num, axis=1)

# On recree les conditions aux limites
from hamopy.classes import Boundary
clim1 = Boundary('Dirichlet',**{"time" : time_new,
                                "T"    : T_CL_down[0],
                                "HR"   : HR_CL_down[0] })
clim2 = Boundary('Dirichlet',**{"time" : time_new,
                                "T"    : T_CL_down[1],
                                "HR"   : HR_CL_down[1] })
clim = [clim1, clim2]


""" Priors """

# Noise priors
#std_noise_T  = pm.Uniform('std of T noise', 0, 0.5, value = 0.1)    # expected value is 0.1
#std_noise_HR = pm.Uniform('std of HR noise', 0, 0.05, value = 0.01) # expected value is 0.01
#std_noise_Q  = pm.Uniform('std of Q noise', 0, 0.1, value = 0.01)    # expected value is 0.01
std_noise_T  = 0.1
std_noise_HR = 0.01
std_noise_Q  = 0.01

# Adding the possibility of noise to boundary condition observations
"""
T_CL_obs = pm.Normal('observed temperature', mu = T_CL_file,
                     tau = 1e10, value = T_CL_file, observed = True)
HR_CL_obs = pm.Normal('observed humidity', mu = HR_CL_file,
                      tau = 1e10, value = HR_CL_file, observed = True)
"""
T_CL_real  = pm.Normal('assumed temperature',  mu = T_CL_down,
                       tau = 1./(std_noise_T**2))
HR_CL_real = pm.Normal('assumed humidity', mu = HR_CL_down,
                       tau = 1./(std_noise_HR**2))

# Parameter priors
lambda_0 = pm.Uniform("lambda_0", 0.02, 0.1)#, value = 0.06)  # expected value is 0.05
lambda_m = pm.Uniform("lambda_m", 0.2, 1, value = 0.6)      # expected value is 0.5
lambda_t = pm.Uniform("lambda_t", 5e-5, 2e-4, value = 1.2e-4) # expected value is 1e-4
cp       = pm.Uniform("cp", 500, 4000, value = 2250)        # expected value is 2000
dp_p1    = pm.Uniform("dp_p1", 2.5e-11, 1e-10, value = 6.5e-11)  # expected value is 5e-11
dp_p2    = pm.Uniform("dp_p2", 5e-11,   2e-10, value = 1.25e-10)  # expected value is 1e-10
#xi_p1    = pm.Uniform("xi_p1", 5, 35, value = 20)           # expected value is 17
#xi_p2    = pm.Uniform("xi_p2", 9, 40, value = 25)           # expected value is 19
#xi_p3    = pm.Uniform("xi_p3", 23, 95, value = 59)          # expected value is 47
xi = pm.Uniform("xi", 0, 100, size = 3)

""" Function """
from hamopy import ham_library as ham
from hamopy.algorithm import calcul
from hamopy.postpro import evolution, heat_flow
from benchmark.benchmark_input_7j_CLbruit import mesh, init, time

def fonction(T_CL, HR_CL, lambda_0, lambda_m, lambda_t, cp,
             dp_p1, dp_p2, xi):
    
    # Material properties    
    m = deepcopy(mesh.materials[0])
    c = deepcopy(clim)
    
    m.set_conduc(lambda_0, lambda_m, lambda_t)
    m.set_capacity(cp)
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [dp_p1, dp_p2]} )
                                   
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : xi  } )
    
    mesh.replace_materials([m])
    
    # Boundary conditions
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
        return np.zeros((7, len(time_new)))
        #return np.zeros(len(t_mesure))
        
    else:
        # Post processing
        """
        T_calcul  = np.array([evolution(resultat_simul, 'T',  x = _, t = time_new) for _ in [0.025, 0.05, 0.075]])
        HR_calcul = np.array([evolution(resultat_simul, 'HR', x = _, t = time_new) for _ in [0.025, 0.05, 0.075]])
        Q_calcul  = heat_flow(resultat_simul, mesh, clim, x = 0.05,  t = time_new)
        """
        T_calcul  = evolution(resultat_simul, 'T',  x = 0.05)
        HR_calcul = evolution(resultat_simul, 'HR', x = 0.05)
        Q_calcul  = heat_flow(resultat_simul, mesh, clim, x = 0.05)
        
        out1 = np.row_stack((T_calcul, HR_calcul, Q_calcul))
        out2 = resample(out1, num, axis=1)
        
        return out2
        #return T_calcul

@pm.deterministic
def calculs(lambda_0 = lambda_0, lambda_m = lambda_m, lambda_t = lambda_t,
            cp = cp, dp_p1 = dp_p1, dp_p2 = dp_p2, xi = xi):
    
    return fonction(T_CL_real, HR_CL_real, lambda_0, lambda_m, lambda_t, cp,
                    dp_p1, dp_p2, xi)

""" Likelihood """

# Standard deviation
precision = np.array([1/std_noise_T**2, 1/std_noise_HR**2, 1/std_noise_Q**2])
taus = np.tile(precision, (len(time_new),1)).T

# Stochastic variable of the observed output
observation = pm.Normal('observation',
                        mu = calculs,
                        tau = taus,
                        value = outputs_down,
                        observed = True)

""" Inference """

"""
R = pm.MCMC([lambda_0, lambda_m, lambda_t, cp, dp_p1, dp_p2, xi_p1, xi_p2, xi_p3],
            db='pickle', dbname='HAM_benchmark.pickle')
"""
R = pm.MCMC([xi, observation],
            db='pickle', dbname='HAM_benchmark.pickle')

R.db
R.sample(100)
R.db.close()

pm.Matplot.plot(R)

"""
lambda_0_samples = R.trace('lambda_0')[:]
lambda_m_samples = R.trace('lambda_m')[:]
lambda_t_samples = R.trace('lambda_t')[:]
cp_samples = R.trace('cp')[:]
dp_p1_samples = R.trace('dp_p1')[:]
dp_p2_samples = R.trace('dp_p2')[:]
xi_p1_samples = R.trace('xi_p1')[:]
xi_p2_samples = R.trace('xi_p2')[:]
xi_p3_samples = R.trace('xi_p3')[:]
np.savetxt('resultats_benchmark.txt', np.array((lambda_0_samples, lambda_m_samples, lambda_t_samples,
                                 cp_samples, dp_p1_samples, dp_p2_samples,
                                 xi_p1_samples, xi_p2_samples, xi_p3_samples )).T)
"""