# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 00:27:28 2022

@author: DELL
"""

import numpy as np
from datetime import datetime

n = 5
n_population = 10
mutation_rate = 0.2
lista_coordenadas= [
    [0, 7, 9, 8, 20],
    [7, 0, 10, 4, 11],
    [9, 10, 0, 15, 5],
    [8, 4, 15, 0, 17],
    [20, 11, 5, 17, 0]
]
lista_nombres = np.array(['A', 'B', 'C', 'D', 'E'])
nodos = {x: y for x, y in zip(lista_nombres, lista_coordenadas)}


def compute_city_distance_coordinates(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) * 0.5


def compute_city_distance_names(ciudad_a, ciudad_b, nodos):
    return compute_city_distance_coordinates(nodos[ciudad_a], nodos[ciudad_b])


def genesis(city_list, n_population):
    population_set = []
    for i in range(n_population):
        sol_i = city_list[np.random.choice(list(range(n)), n, replace=False)]
        population_set.append(sol_i)
    return np.array(population_set)

population_set = genesis(lista_nombres, n_population)


def fitness_eval(city_list, nodos):
    total = 0
    for i in range(n - 1):
        a = city_list[i]
        b = city_list[i + 1]
        total += compute_city_distance_names(a, b, nodos)
    return total


def get_all_fitnes(population_set, nodos):
    fitnes_list = np.zeros(n_population)

    for i in range(n_population):
        fitnes_list[i] = fitness_eval(population_set[i], nodos)

    return fitnes_list


fitnes_list = get_all_fitnes(population_set, nodos)


def progenitor_selection(population_set, fitnes_list):
    total_fit = fitnes_list.sum()
    prob_list = fitnes_list / total_fit

    progenitor_list_a = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list,
                                         replace=True)
    progenitor_list_b = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list,
                                         replace=True)

    progenitor_list_a = population_set[progenitor_list_a]
    progenitor_list_b = population_set[progenitor_list_b]

    return np.array([progenitor_list_a, progenitor_list_b])


progenitor_list = progenitor_selection(population_set, fitnes_list)


def mate_progenitors(prog_a, prog_b):
    offspring = prog_a[0:5]

    for city in prog_b:

        if not city in offspring:
            offspring = np.concatenate((offspring, [city]))

    return offspring


def mate_population(progenitor_list):
    new_population_set = []
    for i in range(progenitor_list.shape[1]):
        prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
        offspring = mate_progenitors(prog_a, prog_b)
        new_population_set.append(offspring)

    return new_population_set


new_population_set = mate_population(progenitor_list)


def mutate_offspring(offspring):
    for q in range(int(n * mutation_rate)):
        a = np.random.randint(0, n)
        b = np.random.randint(0, n)

        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(new_population_set):
    mutated_pop = []
    for offspring in new_population_set:
        mutated_pop.append(mutate_offspring(offspring))
    return mutated_pop


mutated_pop = mutate_population(new_population_set)

solucion = [-1, np.inf, np.array([])]
for i in range(10000):
    if i % 100 == 0: print(i, fitnes_list.min(), fitnes_list.mean(), datetime.now().strftime("%d/%m/%y %H:%M"))
    fitnes_list = get_all_fitnes(mutated_pop, nodos)

    if fitnes_list.min() < solucion[1]:
        solucion[0] = i
        solucion[1] = fitnes_list.min()
        solucion[2] = np.array(mutated_pop)[fitnes_list.min() == fitnes_list]

    progenitor_list = progenitor_selection(population_set, fitnes_list)
    new_population_set = mate_population(progenitor_list)

    mutated_pop = mutate_population(new_population_set)

hof = solucion[2][0]

print("Ruta mas corta :")

for i in range(len(hof) - 1):
    print(hof[i], "=>", hof[(i + 1) % 5])
