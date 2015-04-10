import numpy as np
from scipy.interpolate import interp1d

""" Space and time discretisation """

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

def T_func(lambda_, xc, u, time_out):    
    
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
    
    # Calcul par resolution du systeme lineaire a chaque pas de temps
    T = T_initial * np.ones((N_samples, N_nodes))
    X = np.eye(N_nodes) - time_step * A
    for t in range(len(time_)-1):
        Y = T[t] + time_step*np.interp(time_[t+1], time_out, u)*b
        T[t+1] = np.linalg.solve(X,Y)
    
    # Interpolation to get the temperature evolution at the sensor position
    #xc = np.min( (np.max((0, xc)),0.05) )
    foo = interp1d(x, T, bounds_error = False, fill_value = 0)
    T_xc = foo(xc)
    # Second interpolation to get this evolution at the time scale of measurements
    return np.interp(time_out, time_, T_xc)

