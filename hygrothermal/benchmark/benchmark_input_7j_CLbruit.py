"""
Fichier d'entree pour la simulation du benchmark numerique d'inversion
"""


from hamopy.classes import Mesh, Boundary, Time

# Choix des materiaux et de la geometrie
from hamopy.materials.virtuel import isolant

"""
isolant.set_capacity(cp_0 = 1963.148)
isolant.set_conduc(lambda_0 = 0.049, lambda_m = 0.514, lambda_t = 1.029e-4)
isolant.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                 "XI" : [20.703, 18.844, 50.068] })
isolant.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                    "dp" : [5.16e-11, 9.947e-11] } )
"""

mesh = Mesh(**{"materials"    : [isolant],
               "sizes"        : [0.1],
               "nbr_elements" : [20] })

# Conditions aux limites
fichier_climat = 'benchmark_mesure_bruit.txt'

clim1 = Boundary('Dirichlet',**{"file" : fichier_climat,
                                "time" : "t (s)",
                                "T"    : "T (x=0)",
                                "HR"   : "HR (x=0)" })

clim2 = Boundary('Dirichlet',**{"file" : fichier_climat,
                                "time" : "t (s)",
                                "T"    : "T (x=10cm)",
                                "HR"   : "HR (x=10cm)" })
clim = [clim1, clim2]

# Conditions initiales
init = {'T'  : 292.15,
        'HR' : 0.5}

# Discretisation temporelle
time = Time('variable',**{"delta_t"  : 600,
                          "t_max"    : 7*24*3600,
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
    x_plot = [0.025, 0.05, 0.075]

    Temperature = np.column_stack([evolution(result, 'T' , _, t_plot) for _ in x_plot])
    Humidite    = np.column_stack([evolution(result, 'HR', _, t_plot) for _ in x_plot])

    from hamopy.postpro import heat_flow
    
    Flux = np.column_stack( heat_flow(result, mesh, clim, x = _, t = t_plot) for _ in [0.05])
