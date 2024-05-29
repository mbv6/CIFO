from random import sample, random, uniform
from classes.population import Population
from classes.individual import Individual
from library.population import rank_population


def tournament_selection(
    population: Population, tournament_size=10, temperature_placeholder=None
) -> Individual:
    """
    Select a certain number of random individuals from the population (without repetition) and select the best one according to its fitness.

    Parameters:
    population (Population): population from which to pick a certain number of random individuals.
    tournament_size (int): number of random individuals to pick from population.
    temperature_placeholder (Any): used to keep same template between all selection function

    Returns:
    Individual: best ranked individual from selected ones
    """
    # Select tournament_size individuals at random (no repetition)
    tournament = sample(population.individuals, tournament_size)
    ranked_tournament = rank_population(tournament)

    return ranked_tournament[0][0]


def fitness_proportionate_selection(
    population: Population,
    tournament_size_placeholder=None,
    temperature_placeholder=None,
) -> Individual:
    """
    Select an individual from the population based on its fitness.
    Individuals with lower fitness have more chance of being selected.

    Parameters:
    population (Population): population from which to pick an individual.
    tournament_size_placeholder (Any): used to keep same template between all selection functions
    temperature_placeholder (Any): used to keep same template between all selection functions

    Returns:
    Individual: selected individual
    """
    total_fitness = sum([individual.fitness for individual in population.individuals])

    probabilities = [
        individual.fitness / total_fitness for individual in population.individuals
    ]

    selected = None
    r = random()
    for i, probability in enumerate(probabilities):
        if r < probability:
            selected = population.individuals[i]
            break
        r -= probability

    return selected


import numpy as np


def boltzmann_selection(
    population: Population, tournament_size_placeholder=None, temperature=1
):
    """
    This selection method is based on entropy and importance sampling methods in Monte Carlo simulation.
    With the selection method, the algorithm can explore as many configurations as possible while exploiting better configurations, consequently helping to solve the premature convergence problem.

    Parameters:
    population (Population): population from which to pick an individual.
    tournament_size_placeholder (Any): used to keep same template between all selection functions
    temperature (Any): adjusting the temperature parameter allows you to control the balance between exploration and exploitation in your genetic algorithm.

    Returns:
    Individual: selected individual

    Note:
    Higher temperatures encourage more exploration, while lower temperatures favor exploitation.
    """
    fitnesses = [individual.get_fitness() for individual in population.individuals]
    # Calculate Boltzmann probabilities
    boltzmann_probabilities = np.exp(np.array(fitnesses) / temperature)
    boltzmann_probabilities /= np.sum(boltzmann_probabilities)

    # Select individuals based on Boltzmann probabilities
    selected_index = np.random.choice(len(population), p=boltzmann_probabilities)
    selected_individual = population[selected_index]

    return selected_individual
