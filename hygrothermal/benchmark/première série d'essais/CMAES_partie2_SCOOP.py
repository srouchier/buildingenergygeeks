# -*- coding: utf-8 -*-
"""
Created on Mon Nov 04 13:44:56 2013

@author: Rouchier
"""
from __future__ import division
import HAMpy  as HAM
import numpy  as np
import pandas as pd
import copy

#############################
### Réglage du modèle HAM ###
#############################

# Conditions de la simulation
from inversion.benchmark_input_isolant_7j import mesh, clim, init, temps

# Choix des matériaux à caractériser
NMATER = [0]
materiaux_initiaux = copy.deepcopy([mesh.materiaux[_] for _ in NMATER])

# Choix des paramètres à identifier et de leurs intervalles de recherche
# parametres est une liste de dictionnaires dans l'ordre de NMATER
parametres = []
# Intervalles de recherche initiaux du premier matériau
parametres.append( {"dp_025"     : [3e-11, 8e-10],
                    "dp_075"     : [5e-11, 1.5e-10],
                    "w_025"      : [5, 10],
                    "w_050"      : [10, 15],
                    "w_075"      : [15, 20] } )

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
capteurs = [0, 0.05, 0.10]

# On spécifie le fichier des mesures et le nom des colonnes à y lire
mesures = pd.read_csv('D:\MCF\Simulation\Python\inversion/benchmark_mesure_isolant2_HR2.txt', delimiter='\t')
t_tags  = 't (s)'
HR_tags = ['HR (x=0)', 'HR (x=5cm)', 'HR (x=10cm)']

# On affecte les mesures aux arrays qui vont bien
t_mesure  = np.array(mesures[t_tags])
HR_mesure = np.column_stack(mesures[_] for _ in HR_tags)

# On coupe les mesures qui dépassent le temps de simulation
HR_mesure = HR_mesure[t_mesure<=temps.fin]
t_mesure  =  t_mesure[t_mesure<=temps.fin]

if len(capteurs) != len(HR_tags):
    Exception('Nombres de capteurs incompatibles')

# Capteurs réels d'humidité
precision_HR = 0
erreur_HR = precision_HR/2*np.random.randn(len(HR_mesure),len(capteurs))
HR_mesure = np.round(HR_mesure + erreur_HR,2)

############################
### Fonctions évaluation ###
############################

# Sauvegarde des propriétés initiales de chaque matériau
prop_init = []

prop_init.append( {'lambda_0'   : 0.05409,
                   'lambda_mst' : 0.137,
                   'lambda_tmp' : 2e-4,
                   'cp'         : 2057.56,
                   'w_025'      : materiaux_initiaux[0].w_025,
                   'w_050'      : materiaux_initiaux[0].w_050,
                   'w_075'      : materiaux_initiaux[0].w_075,
                   'dp_025'     : materiaux_initiaux[0].dp_025,
                   'dp_075'     : materiaux_initiaux[0].dp_075 } )

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
    m.set_conduc(p['lambda_0'], p['lambda_mst'], p['lambda_tmp'])
    
    m.set_capacity(p['cp'])
    
    m.set_perm_vapeur('interp', **{"HR" : [0.25, 0.75],
                                   "dp" : [p['dp_025'], p['dp_075']]} )
                                   
    m.set_isotherme('polynome',**{"HR" : [0, 0.25, 0.5, 0.75],
                                  "W"  : [0, p['w_025'], p['w_050'], p['w_075']] } )
    return m

def evaluation(individual):
    
    # Création des nouveaux matériaux d'après le génotype de l'individu
    mater = copy.deepcopy(materiaux_initiaux)
    for MINDEX in NMATER:
        mater[MINDEX] = modif_materiaux(individual, MINDEX)
    
    # Modification des matériaux dans la classe maillage
    if type(mater) == list:
        mesh.nouveaux_materiaux(mater)
    else:
        mesh.nouveaux_materiaux([mater])
    
    # Simulation
    resultat_simul = HAM.calcul(mesh, clim, init, temps, output_type='dict')
    
    if not type(resultat_simul)==dict:
        
        return (np.inf, )
        
    else:
        # Résultats au point de mesure, avec le même échantillonage du temps
        HR_calcul = np.column_stack( HAM.postpro.evolution(resultat_simul, 'HR', x = p, t = t_mesure) for p in capteurs )
        
        # Résidus : moindres carrés entre mesure et calcul, pondérés par l'amplitude
        R_HR = np.sum( (HR_mesure - HR_calcul)**2 ) / np.mean(HR_mesure)**2
    
        return (R_HR, )
    

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
    NGENMAX = 1000
    
    # Enregistrement de la stratégie
    strategy = cma.Strategy(centroide_initial, sigma=0.5, lambda_=12)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    
    from scoop import futures
    toolbox.register("map", futures.map)
    
    # Statistiques
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)
    hof_complet = np.zeros( (NGENMAX,len(centroide_initial)) )
    stats_pop   = np.zeros( (NGENMAX,len(centroide_initial)) )
   
    column_names = ["gen", "evals"]
    if stats is not None:
        column_names += stats.functions.keys()
    logger = tools.EvolutionLogger(column_names)
    logger.logHeader()
    
    # Algorithme
    STOP = False
    gen = 0
    while not STOP:
        # Generate a new population
        population = toolbox.generate()
        # Ecart type de chaque parametre de la population (normé sur la moyenne)
        foo = np.array(population)
        stats_pop[gen] = np.abs( np.std(foo,axis=0) / np.mean(foo,axis=0) )
        
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
        stats.update(population)
        
        logger.logGeneration(evals=len(population), gen=gen, stats=stats)
        
        gen +=1
        
        # On vérifie si on doit s'arrêter
        conv_paras   = np.max(stats_pop[gen-1]) < 1e-3
        if conv_paras or gen >= NGENMAX:
            STOP = True
    
    return population, stats, stats_pop, hof, hof_complet
    
if __name__ == "__main__":
    
    # print 'Erreur systématique : [%s]' % ', '.join(map(str, accuracy))
    pop, stats, stats_pop, hof, hof_complet = main()
    
    # Mise en forme des résultats
    OptGlobal = []
    OptParGen = np.zeros(np.shape(hof_complet))
    Ecartypes = stats_pop
    for MINDEX in NMATER:
        
        foo = parametres[MINDEX].keys()
        bar = parametres[MINDEX].values()
        OptGlobal.append({})
        
        for i in range(len(para_indices[MINDEX])):
            I = para_indices[MINDEX][i]
            OptGlobal[MINDEX][foo[i]] = bar[i][0] + hof.items[0][I] *(bar[i][1]-bar[i][0])
            OptParGen[:,I] = bar[i][0] + hof_complet[:,I]*(bar[i][1]-bar[i][0])

    # On garde les statistiques intéressantes
    sigma_f = np.array( stats.data['std'][0] )
    moyenne = np.array( stats.data['avg'][0] )
    minimum = np.array( stats.data['min'][0] )
    gen = len(sigma_f)
    
    # Ecriture des résultats dans des fichiers txt
    meilleur = np.column_stack((OptGlobal[_].values() for _ in NMATER))
    np.savetxt('CMAES_partie2_bestfit.txt', meilleur)
    np.savetxt('CMAES_partie2_bestfit_tag.txt', OptGlobal[0].keys(), fmt="%s")
    total = np.column_stack((sigma_f, moyenne, minimum, OptParGen[:gen], Ecartypes[:gen]))
    np.savetxt('CMAES_partie2_stats.txt', total)
    