import numpy as np
from random import randint, sample, random
from copy import deepcopy


# SELECTION METHODS
def tournament_selection(population, k=3):
    """Selects the best individual out of k random individuals."""
    return max(sample(population.individuals, k), key=lambda ind: ind.fitness)



# CROSSOVER METHODS
def single_point_crossover(parent1, parent2):
    """Performs single-point crossover."""
    point = randint(0, 8)
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)
    child1.values[point:], child2.values[point:] = parent2.values[point:], parent1.values[point:]
    return child1, child2

# MUTATION METHODS
def binary_mutation(individual, mutation_rate=0.1):
    """Mutates an individual by swapping two elements within a row with a certain probability."""
    for row in range(9):
        if random() < mutation_rate:
            col1, col2 = sample(range(9), 2)
            while individual.values[row][col1] == 0 or individual.values[row][col2] == 0:
                col1, col2 = sample(range(9), 2)
            individual.values[row][col1], individual.values[row][col2] = individual.values[row][col2], individual.values[row][col1]



