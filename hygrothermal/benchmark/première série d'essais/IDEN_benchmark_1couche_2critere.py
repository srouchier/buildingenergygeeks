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
from hamopy.postpro import evolution

#############################
### Réglage du modèle HAM ###
#############################

# Conditions de la simulation
from inversion.benchmark_input_isolant_48h import mesh, clim, init, time

# Choix des matériaux à caractériser
NMATER = [0]
materiaux_initiaux = copy.deepcopy([mesh.materials[_] for _ in NMATER])

# Choix des paramètres à identifier et de leurs intervalles de recherche
# parametres est une liste de dictionnaires dans l'ordre de NMATER
parametres = []
# Intervalles de recherche initiaux du premier matériau
parametres.append( {"lambda_0" : [0.02, 0.08],
                    "lambda_m" : [0.1, 0.5],
                    "lambda_t" : [5e-5, 1.5e-4],
                    "cp"       : [1000, 3000],
                    "dp_025"   : [3e-11, 8e-10],
                    "dp_075"   : [5e-11, 1.5e-10],
                    "w_025"    : [5, 8],
                    "w_050"    : [9, 14],
                    "w_075"    : [16, 22] })

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

###########################
### Mesures de contrôle ###
###########################

# Position des capteurs : liste de coordonnées
capteurs = [0, 0.025, 0.05, 0.075, 0.1]

# On spécifie le fichier des mesures et le nom des colonnes à y lire
mesures = pd.read_csv('D:\MCF\Simulation\Python\inversion/benchmark_mesure_isolant2.txt', delimiter='\t')
t_tags  = 't (s)'
T_tags  = ['T (x=0)', 'T (x=2.5cm)', 'T (x=5cm)', 'T (x=7.5cm)', 'T (x=10cm)']
HR_tags = ['HR (x=0)', 'HR (x=2.5cm)', 'HR (x=5cm)', 'HR (x=7.5cm)', 'HR (x=10cm)']

# On affecte les mesures aux arrays qui vont bien
t_mesure  = np.array(mesures[t_tags])
T_mesure  = np.column_stack(mesures[_] for _ in T_tags)
HR_mesure = np.column_stack(mesures[_] for _ in HR_tags)

# On coupe les mesures qui dépassent le temps de simulation
T_mesure  =  T_mesure[t_mesure<=time.end]
HR_mesure = HR_mesure[t_mesure<=time.end]
t_mesure  =  t_mesure[t_mesure<=time.end]

N = len(t_mesure)
C = len(capteurs)

if len(capteurs) != len(T_tags) or len(capteurs) != len(HR_tags):
    Exception('Nombres de capteurs incompatibles')

# Capteurs réels d'humidité
precision_HR = 0
erreur_HR = precision_HR/2*np.random.randn(len(HR_mesure),len(capteurs))
HR_mesure = np.round(HR_mesure + erreur_HR,2)

# Capteurs réels de température
precision_T = 0
erreur_T = precision_T/2*np.random.randn(len(HR_mesure),len(capteurs))
T_mesure = np.round(T_mesure + erreur_T,1)

# Pondération des capteurs
w_T  = 1
w_HR = 1

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
                       'w_025'    : materiaux_initiaux[m].w_025,
                       'w_050'    : materiaux_initiaux[m].w_050,
                       'w_075'    : materiaux_initiaux[m].w_075,
                       'dp_025'   : materiaux_initiaux[m].dp_025,
                       'dp_075'   : materiaux_initiaux[m].dp_075 } )

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
                                  "dp" : [p['dp_025'], p['dp_075']]} )
                                   
    m.set_isotherm('polynomial', **{"HR" : [0, 0.25, 0.5, 0.75],
                                    "W"  : [0, p['w_025'], p['w_050'], p['w_075']]  } )
                                   
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
        
        return (np.inf, np.inf )
        
    else:
        # Résultats au point de mesure, avec le même échantillonage du temps
        T_calcul  = np.column_stack( evolution(resultat_simul, 'T',  x = p, t = t_mesure) for p in capteurs )
        HR_calcul = np.column_stack( evolution(resultat_simul, 'HR', x = p, t = t_mesure) for p in capteurs )
        
        # Moindres carrés entre mesure et calcul
        mc_T  = 1./N * np.sum( (T_mesure  - T_calcul)**2, axis=0 )
        mc_HR = 1./N * np.sum( (HR_mesure - HR_calcul)**2, axis=0 )
        
        # Les résidus sont rapportés sur les valeurs moyennes des mesures
        R_T   = 1./C * np.sum( mc_T  / np.mean(T_mesure, axis=0)**2 )
        R_HR  = 1./C * np.sum( mc_HR / np.mean(HR_mesure, axis=0)**2 )
        
        # Pondération
        R_T  *= w_T
        R_HR *= w_HR
    
        return (R_HR, R_T)
    

############################
### Les choses sérieuses ###
############################

from deap import creator, base, tools, cma

creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", evaluation)

def main():

    # Nombre max de générations
    NGENMAX = 2000
    
    # Enregistrement de la stratégie
    strategy = cma.Strategy(centroide_initial, sigma=0.3, lambda_=12)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    
    # Pour utiliser SCOOP il faut ca
    from scoop import futures
    toolbox.register("map", futures.map)
    
    # Statistiques
    hof = tools.HallOfFame(1)
    par = tools.ParetoFront()
    
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
        
        # Ecart type de chaque parametre de la population (normé sur la moyenne)
        foo = np.array(population)
        ecartypes[gen] = np.abs( np.std(foo,axis=0) / np.mean(foo,axis=0) )
        
        # Evaluate the individuals
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # Update hall of fame
        hof.update(population)
        par.update(population)
        hof_complet[gen] = hof.items[0]
        
        # Update the strategy with the evaluated individuals
        toolbox.update(population)
        
        # Update statistics
        record = stats.compile(population)
        logbook.record(gen=gen, evals=len(population), **record)
        print logbook.stream
        
        gen +=1
        
        # On vérifie si on doit s'arrêter
        conv_paras = np.max(ecartypes[gen-1]) < 1e-3
        if conv_paras or gen >= NGENMAX:
            STOP = True
    
    # Calcul du fitness de chaque élément du front de pareto
    par_fit = list( toolbox.map(toolbox.evaluate, par) )
    
    return logbook, ecartypes, hof, hof_complet, par, par_fit
    
if __name__ == "__main__":
    
    # print 'Erreur systématique : [%s]' % ', '.join(map(str, accuracy))
    logbook, ecartypes, hof, hof_complet, par, par_fit = main()
    
    pareto = np.array(par.items)
    ParFit = np.array(par_fit)
    
    # Mise en forme des résultats
    # ATTENTION : l'ordre des paramètres n'est pas le même dans OptGlobal que
    # dans OptParGen et OptPareto
    OptGlobal = []
    OptPareto = np.zeros(np.shape(pareto))
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
            OptPareto[:,I] = bar[i][0] + pareto[:,I] * (bar[i][1]-bar[i][0])
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
    
    # Front de Pareto
    toutpareto = np.column_stack((OptPareto, ParFit))
    np.savetxt('IDEN_pareto.txt', toutpareto)
    