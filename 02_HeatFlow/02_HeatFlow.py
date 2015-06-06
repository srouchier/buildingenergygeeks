
import numpy as np

""" Physical settings """

# Space discretisation
N = 21                  # number of nodes in the mesh
delta_x = 0.05 / (N-1)  # spacing between nodes

# Material properties
lambda_ = 0.3           # heat conductivity
rho_cp  = 1.2e6         # heat capacity
a = lambda_ / rho_cp    # heat diffusivity

# Initial and boundary conditions
h = 0                   # surface transfer coefficient on the right boundary
T_initial = 0           # initial temperature
Biot = h * delta_x / lambda_

""" Input data """

# Reading the input file
import pandas
data_ = pandas.read_csv('input_file.txt', delimiter='\t')
time_ = np.array(data_['t (s)'])    # time discretisation
K     = len(time_)                  # number of time steps

# Temperature measurements with added noise
T_obs    = np.array(data_['T(e/2)'])
T_obs += np.random.normal(0, 0.2, size=np.size(T_obs))

# Vector that specifies where the sensor is
C = np.zeros(N)
C[10] = 1

""" Setting up the system"""

# Matrices A et b
diag_moy = -2*np.ones(N)
diag_sup = np.ones(N-1)
diag_inf = np.ones(N-1)
diag_moy[-1] += -2*Biot
diag_sup[0]  += 1
diag_inf[-1] += 1
A = a / delta_x**2 * (np.diag(diag_moy)+np.diag(diag_inf, k=-1)+np.diag(diag_sup, k=1))
b = np.zeros(N)
b[0] += 2./(rho_cp * delta_x)

""" Setting up the sensitivity matrix """ 

n = 20                                  # number of modes for the discretisation of u
time_n = np.linspace(0, time_[-1], n)

# Une fonction f
def f_hat(t, j, time_n):
    
    delta_t = np.diff(time_n).mean()
    
    f_rise = (t-time_n[j-1]) / delta_t
    f_decr = 1 - (t-time_n[j]) / delta_t
    
    if j == 0:
        is_rise = False
    else:
        is_rise = (t >= time_n[j-1]) * (t <= time_n[j])
        
    if j == len(time_n)-1:
        is_decr = False
    else:
        is_decr = (t >= time_n[j]) * (t <= time_n[j+1])
    
    return f_rise * is_rise + f_decr * is_decr


# The initial time t0 doesnt appear in S, so the matrix has one less line
S = np.zeros((K-1, n-1))
from scipy.linalg import expm

time_indices = range(K)
for t in time_indices[1:]:
    
    tau   = time_[:t+1]
    
    for j in range(n-1):
        
        f_tau = f_hat(tau, j, time_n)
        # Calculate an integral for each value of S
        foo = np.zeros(len(tau))
        for i in range(len(tau)):
            # This is a scalar
            foo[i] = np.dot(C, np.dot( expm(A*(time_[t]-tau[i])), b)) * f_tau[i]
        S[t-1,j] = np.trapz(foo, tau)

""" Solving """

u_modes = np.linalg.solve(np.dot(S.T, S), np.dot(S.T, T_obs[1:]))

U = np.zeros(K)

for j in range(n-1):
    U += u_modes[j] * f_hat(time_, j, time_n)
    
""" Validation """

u_true = data_['U (W/m2)']
# Graphes
import matplotlib.pylab as plt
from matplotlib import rc
rc("font", family="serif", size=14)

plt.hold(True)
plt.plot(time_, u_true, '-k')
plt.plot(time_, U, 'or-')
plt.xlabel('Time (s)')
plt.ylabel('Heat flow (W/m2)')
plt.legend(('Target', 'Estimated'))