# This file uses hamopy
# http://srouchier.github.io/hamopy/

from hamopy.classes import Mesh, Boundary, Time

#==============================================================================
# Choice of materials and geometry
#==============================================================================
from hamopy.materials.virtuel import isolant

h = 0.08    # hauteur de l'eprouvette
D = 0.111   # diametre de l'eprouvette
                                  
mesh = Mesh(**{"materials"    : [isolant],
               "sizes"        : [h],
               "nbr_elements" : [23] })

#==============================================================================
# Boundary conditions
#==============================================================================
fichier_climat = 'measurements.txt'
import pandas
data = pandas.read_csv(fichier_climat, delimiter = '\t')

clim1 = Boundary('Fourier',**{"file" : fichier_climat,
                                "time" : "Time (s)",
                                "T"    : "T ext",
                                "HR"   : "RH ext",
                                "h_m"  : 7.45e-9})

clim2 = Boundary('Fourier',**{"file" : fichier_climat,
                                "time" : "Time (s)",
                                "T"    : "T ext",
                                "HR"   : "RH ext",
                                "h_t"  : 0,
                                "h_m"  : 0})
clim = [clim1, clim2]

#==============================================================================
# Initial conditions
#==============================================================================

init = {'T'  : data['T'][0],
        'HR' : 0.065}

#==============================================================================
# Time step
#==============================================================================
time = Time('variable',**{"delta_t"  : 600,
                          "t_max"    : data['Time (s)'].max(),
                          "iter_max" : 12,
                          "delta_min": 1e-3,
                          "delta_max": 4*3600 } )
#==============================================================================
# Main
#==============================================================================
if __name__ == "__main__":
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Calculation
    from hamopy.algorithm import calcul
    result = calcul(mesh, clim, init, time)
    
    # Post processing
    from hamopy.postpro import evolution, distribution
    t_plot = data['Time (s)'].values
    
    # H is the relative humidity in the middle of a sample
    x_plot = [h]
    H = np.column_stack([evolution(result, 'HR', _, t_plot) for _ in x_plot])
    
    plt.figure()
    plt.plot(t_plot/3600, data['RH1'], '-k', label = 'Measurements')
    plt.plot(t_plot/3600, H, '-r', label = 'Simulation')
    plt.xlabel('Time (h)')
    plt.ylabel('Relative humidity')
    plt.legend(loc='lower right')
    
    # Masse
    import hamopy.ham_library as ham
    x_integ = np.linspace(0, h)
    W = np.zeros_like(t_plot)
    for i in range(len(t_plot)):
        hum = distribution(result, 'HR', x_integ, t_plot[i])
        tem = distribution(result, 'T', x_integ, t_plot[i])
        w_integ = isolant.w(ham.p_c(hum,tem), tem)
        W[i] = np.trapz(y = w_integ, x = x_integ)
    W *= W * np.pi*D**2/4*1000 # pour passer de (kg/m2) a des (g)
    W -= W[0]
    
    plt.figure()
    plt.plot(t_plot/3600, data['Mass (g)'] - data['Mass (g)'][0], '-k', label = 'Measurements')
    plt.plot(t_plot/3600, W, 'r', label = 'Simulation')
    plt.xlabel('Time (h)')
    plt.ylabel('Water content (kg/m3)')
    plt.legend(loc='lower right')