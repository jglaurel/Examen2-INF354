# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 00:24:54 2022

@author: DELL
"""

from deap import creator, base, tools, algorithms
import numpy as np
toolbox = base.Toolbox()
n = 5

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("EstrIndividuo", list, fitness=creator.FitnessMin)
toolbox.register("Genes", np.random.permutation, n)
toolbox.register("Individuos", tools.initIterate, creator.EstrIndividuo, toolbox.Genes)
toolbox.register("Populacao", tools.initRepeat, list, toolbox.Individuos)
pop = toolbox.Populacao(n=10)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=2)
dist = [
    [0, 7, 9, 8, 20],
    [7, 0, 10, 4, 11],
    [9, 10, 0, 15, 5],
    [8, 4, 15, 0, 17],
    [20, 11, 5, 17, 0]
]

def apt(individuo):
    f = 0
    for i in range(n-1):
        local1 = individuo[i]
        local2 = individuo[i+1]
        distancia = dist[local1][local2]
        f = f + distancia
    return f,


toolbox.register("evaluate", apt)


def estadisticaGuardada(individuo):
    return individuo.fitness.values


estadistica = tools.Statistics(estadisticaGuardada)
estadistica.register('mean', np.mean)
estadistica.register('min', np.min)
estadistica.register('max', np.max)

hof = tools.HallOfFame(1)

resultado, log = algorithms.eaSimple(
    pop,
    toolbox,
    cxpb=0.8,
    mutpb=0.1,
    stats=estadistica,
    ngen=30,
    halloffame=hof,
    verbose=True
)
print("------------Resultados---------------")
print(resultado)
print("------------Mejor Camino---------------")
print(hof)

menor = hof[0]
print("------------Distancia Minima---------------")
print(apt(menor))