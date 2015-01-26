# -*- coding: utf-8 -*-
"""
Created on Mon Nov 04 13:44:56 2013

@author: Rouchier
"""
from __future__ import division
import numpy  as np
import pandas as pd
import copy

from hamopy.algorithm import calcul
from hamopy.postpro import evolution, heat_flow

#############################
### Réglage du modèle HAM ###
#############################

# Conditions de la simulation
from inversion_benchmark.benchmark_input_7j_CLbruit import mesh, clim, init, time

# Choix des matériaux à caractériser
NMATER = [0]
materiaux_initiaux = copy.deepcopy([mesh.materials[_] for _ in NMATER])

# Choix des paramètres à identifier et de leurs intervalles de recherche
# parametres est une liste de dictionnaires dans l'ordre de NMATER
parametres = []
# Intervalles de recherche initiaux du premier matériau
parametres.append( {"lambda_0" : [0.02, 0.1],
                    "lambda_m" : [0.2, 1],
                    "lambda_t" : [5e-5, 2e-4],
                    "cp"       : [500, 4000],
                    "dp_p1"    : [2.5e-11, 1e-10],
                    "dp_p2"    : [5e-11, 2e-10],
                    "xi_p1"    : [5, 35],
                    "xi_p2"    : [9, 40],
                    "xi_p3"    : [23, 95] })

if len(parametres) != len(NMATER):
    Exception("Donner autant de jeux de paramètres que de matériaux à identifier")

# Liste des indices correspondant à chaque matériau dans un individu
para_indices = []
imin = 0
for u in range(len(parametres)):
    imax = len(parametres[u])
    para_indices.append(range(imin, imin+imax))
    imin = imax
    
centroide_initial = [0.5] * sum( len(parametres[_].items()) for _ in NMATER )
initial_guess = np.array(centroide_initial)

###########################
### Mesures de contrôle ###
###########################

# Position des capteurs : liste de coordonnées
capteurs = [0.025, 0.05, 0.075]
capteurs_flux = [0.05]

# On spécifie le fichier des mesures et le nom des colonnes à y lire
mesures = pd.read_csv('D:\MCF\Simulation\Python\inversion_benchmark/benchmark_mesure_bruit.txt', delimiter='\t')
t_tags  = 't (s)'
T_tags  = ['T (x=2.5cm)', 'T (x=5cm)', 'T (x=7.5cm)']
HR_tags = ['HR (x=2.5cm)', 'HR (x=5cm)', 'HR (x=7.5cm)']
Q_tags  = ['Q (x=5cm)']

# On affecte les mesures aux arrays qui vont bien
t_mesure  = np.array(mesures[t_tags])
T_mesure  = np.column_stack(mesures[_] for _ in T_tags)
HR_mesure = np.column_stack(mesures[_] for _ in HR_tags)
Q_mesure  = np.column_stack(mesures[_] for _ in Q_tags)

# On coupe les mesures qui dépassent le temps de simulation
T_mesure  =  T_mesure[t_mesure<=time.end]
HR_mesure = HR_mesure[t_mesure<=time.end]
Q_mesure  =  Q_mesure[t_mesure<=time.end]
t_mesure  =  t_mesure[t_mesure<=time.end]

N = len(t_mesure)
C = len(capteurs)
C_flux = len(capteurs_flux)

if len(capteurs) != len(T_tags) or len(capteurs) != len(HR_tags):
    Exception('Nombres de capteurs incompatibles')

# Pondération des capteurs
resol_T  = [0.2] * C
resol_HR = [0.01] * C
resol_Q  = [0.1] * C_flux

w_T  = 1. / np.array(resol_T)**2
w_HR = 1. / np.array(resol_HR)**2
w_Q  = 1. / np.array(resol_Q)**2

############################
### Fonctions évaluation ###
############################

# Sauvegarde des propriétés initiales de chaque matériau
prop_init = []
for m in NMATER:
    prop_init.append( {'lambda_0' : materiaux_initiaux[m].lambda_0,
                       'lambda_m' : materiaux_initiaux[m].lambda_m,
                       'lambda_t' : materiaux_initiaux[m].lambda_t,
                       'cp'       : materiaux_initiaux[m].cp_0,
                       'xi_p1'    : materiaux_initiaux[m].xi_p1,
                       'xi_p2'    : materiaux_initiaux[m].xi_p2,
                       'xi_p3'    : materiaux_initiaux[m].xi_p3,
                       'dp_p1'   : materiaux_initiaux[m].dp_p1,
                       'dp_p2'   : materiaux_initiaux[m].dp_p2 } )

# Fonction de modification d'un matériau
def modif_materiaux(individual, MINDEX):
    """
    La fonction retourne un nouveau matériau m
    
    p : dictionnaire de l'ensemble des propriétés, modifiées d'après l'individu
    ou identiques aux propriétés initiales
    """
    
    # Partie de l'individu qui concerne le matériau à modifier
    indiv_reduit = [individual[_] for _ in para_indices[MINDEX]]
    
    # Sauvegarde des données initiales pour pouvoir les modifier tranquillement
    m = copy.deepcopy( materiaux_initiaux[MINDEX] )
    p = copy.deepcopy( prop_init[MINDEX] )
    k = parametres[MINDEX].keys()
    v = parametres[MINDEX].values()
    
    # Les nouvelles données (individual) sont intégrées dans le dictionnaire p
    for i in range(len(indiv_reduit)):
        p[k[i]] = v[i][0] + indiv_reduit[i]*(v[i][1]-v[i][0])
    
    # Le nouveau matériau est créé
    m.set_conduc(p['lambda_0'], p['lambda_m'], p['lambda_t'])
    
    m.set_capacity(p['cp'])
    
    m.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                  "dp" : [p['dp_p1'], p['dp_p2']]} )
                                   
    m.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                               "XI" : [p['xi_p1'], p['xi_p2'], p['xi_p3']]  } )
                                   
    return m

def evaluation(individual):
    
    # Création des nouveaux matériaux d'après le génotype de l'individu
    mater = copy.deepcopy(materiaux_initiaux)
    for MINDEX in NMATER:
        mater[MINDEX] = modif_materiaux(individual, MINDEX)
    
    # Modification des matériaux dans la classe maillage
    if type(mater) == list:
        mesh.replace_materials(mater)
    else:
        mesh.replace_materials([mater])
    
    # Simulation
    resultat_simul = calcul(mesh, clim, init, time)
    
    if not type(resultat_simul)==dict:
        
        return (np.inf, )
        
    else:
        # Résultats au point de mesure, avec le même échantillonage du temps
        T_calcul  = np.column_stack( evolution(resultat_simul, 'T',  x = p, t = t_mesure) for p in capteurs )
        HR_calcul = np.column_stack( evolution(resultat_simul, 'HR', x = p, t = t_mesure) for p in capteurs )
        Q_calcul  = np.column_stack( heat_flow(resultat_simul, mesh, clim, x = _, t = t_mesure) for _ in capteurs_flux)
        
        # Moindres carrés entre mesure et calcul, total sur chaque capteur
        mc_T  = 1./N * np.sum( (T_mesure  - T_calcul)**2, axis=0 )
        mc_HR = 1./N * np.sum( (HR_mesure - HR_calcul)**2, axis=0 )
        mc_Q  = 1./N * np.sum( (Q_mesure  - Q_calcul)**2, axis=0 )
        
        # Somme des résidus de chaque capteur avec sa pondération
        R_T  = 1./C * np.sum( w_T * mc_T )
        R_HR = 1./C * np.sum( w_HR * mc_HR )
        R_Q  = 1./C_flux * np.sum( w_Q * mc_Q )
        
        # Regularisation
        alpha = 0.1
        normX = np.sum( (np.array(individual)-initial_guess)**2 ) / len(individual)
        
        return (R_T + R_HR + R_Q + alpha*normX, )
    

############################
### Les choses sérieuses ###
############################

from deap import creator, base, tools, cma

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", evaluation)

def main():

    # Nombre max de générations
    NGENMAX = 2000
    
    # Enregistrement de la stratégie
    strategy = cma.Strategy(centroide_initial, sigma=0.3, lambda_=18)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    
    # Pour utiliser SCOOP il faut ca
    from scoop import futures
    toolbox.register("map", futures.map)
    
    # Statistiques
    hof   = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    hof_complet = np.zeros( (NGENMAX,len(centroide_initial)) )
    ecartypes   = np.zeros( (NGENMAX,len(centroide_initial)) )
    
    # Initialisation du logbook
    column_names = ["gen", "evals"]
    if stats is not None:
        column_names += stats.functions.keys()
    logbook = tools.Logbook()
    logbook.header = column_names
    
    # Algorithme
    STOP = False
    gen = 0
    while not STOP:
        
        # Generate a new population
        population = toolbox.generate()
        
        # Ecartype/moyenne de chaque parametre de la population
        foo = np.array(population)
        ecartypes[gen] = np.abs( np.std(foo,axis=0) / np.mean(foo,axis=0) )
        
        # Evaluate the individuals
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Update hall of fame
        hof.update(population)
        hof_complet[gen] = hof.items[0]
        
        # Update the strategy with the evaluated individuals
        toolbox.update(population)
        
        # Update statistics
        record = stats.compile(population)
        logbook.record(gen=gen, evals=len(population), **record)
        print(logbook.stream)
        
        gen +=1
        
        # On vérifie si on doit s'arrêter
        conv_paras   = np.max(ecartypes[gen-1]) < 1e-3
        conv_fitness = (record['std'][-1] / record['avg'][-1]) < 1e-5
        if (conv_paras and conv_fitness) or gen >= NGENMAX:
            STOP = True
    
    return logbook, ecartypes, hof, hof_complet
    
if __name__ == "__main__":
    
    # print 'Erreur systématique : [%s]' % ', '.join(map(str, accuracy))
    logbook, ecartypes, hof, hof_complet = main()
    
    # Mise en forme des résultats
    # ATTENTION : l'ordre des paramètres n'est pas le même dans OptGlobal que
    # dans OptParGen
    OptGlobal = []
    OptParGen = np.zeros(np.shape(hof_complet))
    Ecartypes = ecartypes
    for MINDEX in NMATER:
        
        foo = parametres[MINDEX].keys()
        bar = parametres[MINDEX].values()
        OptGlobal.append({})
        
        for i in range(len(para_indices[MINDEX])):
            I = para_indices[MINDEX][i]
            # Les paramètres d'OptGlobal sont dans l'ordre de foo
            OptGlobal[MINDEX][foo[i]] = bar[i][0] + hof.items[0][I] *(bar[i][1]-bar[i][0])
            # Les paramètres d'OptParGen sont dans l'ordre initial des individus
            OptParGen[:,I] = bar[i][0] + hof_complet[:,I]*(bar[i][1]-bar[i][0])

    # On garde les statistiques intéressantes
    sigma_f = np.array( logbook.select("std") )
    minimum = np.array( logbook.select("min") )
    ngen = len(sigma_f)
    
    # Sauvegarde du meilleur individu et de l'ordre de ses propriétés
    meilleur = np.column_stack((OptGlobal[_].values() for _ in NMATER))
    np.savetxt('IDEN_bestfit.txt', meilleur)
    np.savetxt('IDEN_bestfit_tag.txt', OptGlobal[0].keys(), fmt="%s")
    
    # Stats totales : fitnesses et meilleur individu de chaque génération
    total = np.column_stack((sigma_f, minimum, OptParGen[:ngen], Ecartypes[:ngen]))
    np.savetxt('IDEN_stats.txt', total)
    
    # Pour la courbe L
    normX = np.sum( (np.array(hof.items[0])-initial_guess)**2 ) / len(hof.items[0])
    print normX