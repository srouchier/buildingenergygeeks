
from __future__ import division
import numpy as np
import pymc as pm
from copy import deepcopy
import matplotlib.pyplot as plt
#==============================================================================
# Observations
#==============================================================================
# Loading text data
import pandas
datafile = pandas.read_csv('mesure_ech1_step1.txt', delimiter = '\t')
time_file = np.array(datafile['Temps (s)'])

# Observations
obs_file = np.array(datafile[['HR1', 'Masse (g)']]).T
obs_file[1] -= obs_file[1,0]

# Information on the noise
std_noise_H = 0.05
std_noise_M  = 0.05

h = 0.08
D = 0.111

#==============================================================================
# Priors
#==============================================================================

s = {'h_m'      : [1e-9, 1e-7],
     'dp_1'     : [2e-12, 2e-10],
     'dp_2'     : [2e-12, 2e-10],
     'xi_1'     : [10, 50],
     'xi_2'     : [10, 50],
     'xi_3'     : [10, 100]}
order = ['h_m', 'dp_1', 'dp_2', 'xi_1', 'xi_2', 'xi_3']
N = len(s)

parameters = pm.Uniform('parameters', lower = 0, upper = 1, size = N)
#parameters = pm.Normal('parameters', mu = 0.5, tau = (3/0.5)**2, size = N) # +-3*sigma = 99.7% dans [0, 1]


a = [7.45e-9, 5e-11, 1e-10, 17, 19, 47]
b = [ (a[i]-s[order[i]][0]) / (s[order[i]][1]-s[order[i]][0]) for i in range(len(a)) ]

#==============================================================================
# Evaluation
#==============================================================================
from hamopy.algorithm import calcul
from hamopy.postpro import evolution, distribution
import hamopy.ham_library as ham
from simul_ech1_step1 import mesh, clim, init, time

time.end = time_file.max()

def fonction(parameters):
    p = [ s[order[i]][0] + parameters[i] * (s[order[i]][1]-s[order[i]][0]) 
            for i in range(len(parameters)) ]
    
    # Condition limite
    clim[0].data['h_m'] = p[0]
    
    # Material properties    
    m = deepcopy(mesh.materials[0])
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [p[1], p[2]] } )                       
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : [p[3], p[4], p[5]]  } )
    mesh.replace_materials([m])

    # Calcul
    #print('One evaluation\n')
    resultat_simul = calcul(mesh, clim, init, time)
    
    if resultat_simul['t'].max() < time_file.max():
        
        print('One of the simulations has failed \n')
        return np.zeros_like(obs_file)
        #return np.zeros(len(t_mesure))
        
    else:
        # Post processing
        
        H_calcul = evolution(resultat_simul, 'HR', h/2, time_file)
        
        
        # Masse
        x_integ = np.linspace(0, h)
        W = np.zeros_like(time_file)
        for i in range(len(time_file)):
            hum = distribution(resultat_simul, 'HR', x_integ, time_file[i])
            tem = distribution(resultat_simul, 'T', x_integ, time_file[i])
            w_integ = m.w(ham.p_c(hum,tem), tem)
            W[i] = np.trapz(y = w_integ, x = x_integ)
        M_calcul = W * np.pi*D**2/4*1000 # pour passer de (kg/m2) a des (g)
        M_calcul -= M_calcul[0]

        return np.row_stack((H_calcul, M_calcul))


@pm.deterministic
def Y_calc(parameters = parameters):
    return fonction(parameters)

#==============================================================================
# Likelihood
#==============================================================================

precision = np.array([1/std_noise_H**2] + [1/std_noise_M**2])
taus = np.tile(precision, (len(time_file),1)).T

# Stochastic variable of the observed output
Y_obs = pm.Normal('observation',
                  mu = Y_calc,
                  tau = taus,
                  value = obs_file,
                  observed = True)

#==============================================================================
# Inference
#==============================================================================

# Creating the model (pas grand chose a changer ici)
M = pm.MCMC([parameters])

scale = 2.4**2 / 9  # d'apres Gelman (1996) cite par Haario (2001)

M.use_step_method(pm.AdaptiveMetropolis,
                  parameters,
                  scales = {parameters:[0.02*scale]*N},
                  delay = 500,
                  interval = 200,
                  greedy = False,
                  shrink_if_necessary = True,
                  verbose = 0)

# Echantillonage
M.sample(10000)

""" Post-process 

# Diagnostic de convergence
pm.Matplot.plot(M)

# Recuperation des chaines et de leurs statistiques
burn = 4000
thin = 1

trace_tout  = M.trace('parameters', chain = None)[:] # chain = None : on garde toutes les chaines
trace_selec = trace_tout[burn::thin,:]
stats_selec = M.stats(variables='parameters', start = burn)

# Traduction des chaines et des stats dans les dimensions des bonnes variables
out_params = np.zeros_like(trace_selec)
for i in range(len(order)):
    p = order[i]
    # Trace des parametres
    out_params[:,i] = s[p][0] + trace_selec[:,i] * (s[p][1]-s[p][0])



# np.savetxt('bench.txt', out_params, fmt = '%.6e', delimiter = '\t')
# np.savetxt('traces_bench.txt', trace_tout, fmt = '%.6e', delimiter = '\t')

"""