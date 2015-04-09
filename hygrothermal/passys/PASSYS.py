# -*- coding: utf-8 -*-
"""
Fichier de simulation d'une cellule PASSYS
"""

import numpy  as np
import pandas as pd
from hamopy.classes import Mesh, Boundary, Time

# Choix des matériaux et de la géométrie
from hamopy.materials.standard import wood_fibre
"""
wood_fibre.set_capacity(cp_0 = 1250, cp_t = 11.271)
wood_fibre.set_conduc(lambda_0 = 0.05, lambda_m = 0.25, lambda_t = 1.250e-4)
wood_fibre.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                    "XI" : [22., 25., 62.5] })
wood_fibre.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                       "dp" : [4.75e-11, 8e-11] } )
"""

mesh = Mesh(**{"materials"    : [wood_fibre],
               "sizes"        : [0.16],
               "nbr_elements" : [16] })

# Conditions aux limites
fichier_climat = 'PASSYS_01.txt'
data0 = pd.read_csv(fichier_climat, delimiter='\t')

clim1 = Boundary('Dirichlet',**{"file"      : fichier_climat,
                                "delimiter" : "\t",
                                "time"      : "temps (s)",
                                "T"         : "T_0",
                                "HR"        : "HR_0" })


clim2 = Boundary('Dirichlet',**{"file"      : fichier_climat,
                                "delimiter" : "\t",
                                "time"      : "temps (s)",
                                "T"         : "T_16",
                                "HR"        : "HR_16" })
clim = [clim1, clim2]

# Conditions initiales : init est un dictionnaire
init = {'x'  : np.array([0, 0.04, 0.08, 0.12, 0.16]),
        'HR' : np.array([0.42, 0.48, 0.56, 0.66, 0.88]),
        'T'  : np.array([297.46, 294.84, 291.28, 287.76, 282.88]) }

# Discrétisation temporelle
time = Time(method = 'variable',**{"delta_t"  : 900,
                                   "t_max"    : max(data0['temps (s)']),
                                   "iter_max" : 12,
                                   "delta_min": 1e-3,
                                   "delta_max": 900 } )

if __name__ == '__main__':
    
    # Calcul
    from hamopy.algorithm import calcul
    resultat = calcul(mesh, clim, init, time)
    
    # Post process
    from hamopy.postpro import evolution
    
    t_plot = np.array( data0['temps (s)'] )
    x_plot = [0.04, 0.08, 0.12]
    
    Temperature = np.column_stack([evolution(resultat, 'T', _, t_plot) for _ in x_plot])
    Humidite = np.column_stack([evolution(resultat, 'HR', _, t_plot) for _ in x_plot])
    
    from hamopy.postpro import heat_flow
    
    Flux = np.column_stack( heat_flow(resultat, mesh, clim, x = _, t = t_plot) for _ in [0.08, 0.16])