
import numpy as np

# Space discretisation
size = 0.05
N_nodes = 21
delta_x = size / (N_nodes-1)
x = np.linspace(0, size, num=N_nodes)

# Material properties, initial and boundary conditions
lambda_ = 0.3
rho_cp  = 1.2e6
a = lambda_ / rho_cp
h_convec = 0
T_initial = 0
Biot = h_convec * delta_x / lambda_

# Données d'entrée
import pandas
data_ = pandas.read_csv('input_to_forward_problem.txt', delimiter='\t')
time_data = data_['t (s)']
u_data = data_['U (W/m2)']

# Time discretisation
time_step = 60.
time_stop = 8000
time_ = np.arange(0., time_stop+time_step, time_step)
N_samples = len(time_)

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

""" Calcul """

# Calcul par résolution du système linéaire à chaque pas de temps
T = T_initial * np.ones((N_samples, N_nodes))
X = np.eye(N_nodes) - time_step * A
for t in range(len(time_)-1):
    Y = T[t] + time_step*np.interp(time_[t+1], time_data, u_data)*b
    T[t+1] = np.linalg.solve(X,Y)

# Calcul par fonctions de Green
from scipy.linalg import expm
T2 = T_initial * np.ones((N_samples, N_nodes))
for t in range(N_samples):
    
    tau   = time_[:t+1]
    u_tau = np.interp(tau, time_data, u_data)
    
    terme_integ = np.zeros((N_nodes, len(tau)))
    for i in range(len(tau)):
        terme_integ[:,i] = np.dot( expm(A*(time_[t]-tau[i])), b) * u_tau[i]
    T2[t] = np.trapz(terme_integ, tau)
    
C = np.zeros(N_nodes)
C[5] = 1

""" Plots """
foo = np.interp(time_data,time_,T[:,5])

plt.hold(True)
plt.plot(time_, T[:,5], '-b')
plt.plot(time_, T[:,10], '-k')
plt.plot(time_, T[:,15], '-r')
