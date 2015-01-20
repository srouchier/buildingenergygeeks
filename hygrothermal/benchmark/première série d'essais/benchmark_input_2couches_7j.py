# -*- coding: utf-8 -*-
"""
Création de 4 objets qui définissent l'ensemble du problème :

mesh    : discrétisation spatiale, choix des matériaux
clim    : conditions aux limites, données climatiques
init    : conditions initiales
temps   : discrétisation temporelle, temps de simulation

"""
from HAMpy.creation import creer_maillage, creer_limite, creer_temps

# Choix des matériaux et de la géométrie
from HAMpy.materiaux.virtuel import porteur2, isolant2

mesh = creer_maillage(**{"materiau" : [porteur2, isolant2],
                         "largeurs" : [0.1, 0.08],
                         "nbr_elem" : [20, 16] })

# Conditions aux limites
fichier_climat = 'D:\MCF\Simulation\Python\inversion/benchmark_climat.txt'

clim1 = creer_limite('Neumann',**{"file"       : fichier_climat,
                                  "delimiteur" : "\t",
                                  "temps"      : "t (s)",
                                  "T"          : "T (K)",
                                  "HR"         : "HR 2",
                                  "h_t"        : 25.})

clim2 = creer_limite('Neumann',**{"T"          : 292.15,
                                  "HR"         : 0.5,
                                  "h_t"        : 8.} )
clim = [clim1, clim2]

# Conditions initiales
init = {'T'  : 292.15,
        'HR' : 0.5}

# Discrétisation temporelle
temps = creer_temps(methode = 'variable',**{"delta_t"  : 600,
                                            "t_max"    : 7*24*3600,
                                            "iter_max" : 12,
                                            "delta_min": 1e-3,
                                            "delta_max": 600 } )