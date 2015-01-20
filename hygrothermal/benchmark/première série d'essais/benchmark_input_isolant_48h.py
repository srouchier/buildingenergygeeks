"""
Fichier d'entree pour la simulation du benchmark numerique d'inversion
"""


from hamopy.classes import Mesh, Boundary, Time

# Choix des materiaux et de la geometrie
from hamopy.materials.virtuel import isolant2
"""
isolant2.set_capacity(1903.94)
isolant2.set_conduc(7.28e-3, 2.85, 2.77e-4)
isolant2.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                    "dp" : [4.76e-11, 9.48e-11] } )
isolant2.set_isotherm('polynomial', **{"HR" : [0, 0.25, 0.5, 0.75],
                                       "W"  : [0, 11.5, 15.9, 24.3] })
"""

mesh = Mesh(**{"materials"    : [isolant2],
               "sizes"        : [0.1],
               "nbr_elements" : [20] })

# Conditions aux limites
fichier_climat = 'D:\MCF\Simulation\Python\inversion/benchmark_climat.txt'

clim1 = Boundary('Fourier',**{"file" : fichier_climat,
                              "time" : "t (s)",
                              "T"    : "T (K)",
                              "HR"   : "HR 2",
                              "h_t"  : 25.})

clim2 = Boundary('Fourier',**{"T"          : 292.15,
                              "HR"         : 0.5,
                              "h_t"        : 8.} )
clim = [clim1, clim2]

# Conditions initiales
init = {'T'  : 292.15,
        'HR' : 0.5}

# Discretisation temporelle
time = Time('variable',**{"delta_t"  : 600,
                          "t_max"    : 2*24*3600,
                          "iter_max" : 12,
                          "delta_min": 1e-3,
                          "delta_max": 600 } )

if __name__ == "__main__":
    
    import numpy  as np
    import pandas as pd
    
    # Calculation
    from hamopy.algorithm import calcul
    result = calcul(mesh, clim, init, time)
    
    # Post processing
    from hamopy.postpro import evolution
    data0 = pd.read_csv(fichier_climat, delimiter='\t')
    t_plot = np.arange(0, time.end + 600, 600)
    x_plot = [0, 0.025, 0.05, 0.075, 0.1]

    Temperature = np.column_stack([evolution(result, 'T', _, t_plot) for _ in x_plot])
    Humidite    = np.column_stack([evolution(result, 'HR', _, t_plot) for _ in x_plot])
    
    # Calcul du flux en surface
    from hamopy.postpro import surface_heat_flow_in
    
    if not result.has_key('PV'):
        q_ext_therm = surface_heat_flow_in(result, mesh, clim, 0, t_plot)
        q_int_therm = surface_heat_flow_in(result, mesh, clim, 1, t_plot)
        HeatFlow = np.column_stack((q_ext_therm,q_int_therm))
        
    else:
        (q_ext_therm, q_ext_total) = surface_heat_flow_in(result, mesh, clim, 0, t_plot)
        (q_int_therm, q_int_total) = surface_heat_flow_in(result, mesh, clim, 1, t_plot)
        HeatFlow = np.column_stack((q_ext_therm,q_ext_total,q_int_therm,q_int_total))
