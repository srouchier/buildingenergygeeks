# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 09:26:10 2015

@author: Rouchier
"""

def temperature_tout(lambda_=lambda_):
    
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
        Y = T[t] + time_step*np.interp(time_[t+1], time_direct, u)*b
        T[t+1] = np.linalg.solve(X,Y)
        
    return T