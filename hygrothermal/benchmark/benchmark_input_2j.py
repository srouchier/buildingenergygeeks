"""
Fichier d'entree pour la simulation du benchmark numerique d'inversion
"""


from hamopy.classes import Mesh, Boundary, Time

# Choix des materiaux et de la geometrie
from hamopy.materials.virtuel import isolant

mesh = Mesh(**{"materials"    : [isolant],
               "sizes"        : [0.1],
               "nbr_elements" : [20] })

# Conditions aux limites
fichier_climat = 'D:\MCF\Simulation\Python\inversion_benchmark/benchmark_climat.txt'

clim1 = Boundary('Dirichlet',**{"file" : fichier_climat,
                                "time" : "t (s)",
                                "T"    : "T ext (K)",
                                "HR"   : "HR ext" })

clim2 = Boundary('Dirichlet',**{"file" : fichier_climat,
                                "time" : "t (s)",
                                "T"    : "T int (K)",
                                "HR"   : "HR int" })
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

    Temperature = np.column_stack([evolution(result, 'T' , _, t_plot) for _ in x_plot])
    Humidite    = np.column_stack([evolution(result, 'HR', _, t_plot) for _ in x_plot])

    from hamopy.postpro import heat_flow
    
    Flux = np.column_stack( heat_flow(result, mesh, clim, x = _, t = t_plot) for _ in [0.05])
