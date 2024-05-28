from random import sample, uniform
from library.population import Population
from library.individual import Individual
from classes.population import rank_population


def tournament_selection(population: Population, tournament_size=5) -> Individual:
    """
    Select a certain number of random individuals from the population (without repetition) and select the best one according to its fitness.

    Parameters:
    population (Population): population from which to pick a certain number of random individuals.
    tournament_size (int): number of random individuals to pick from population.

    Returns:
    Individual: best ranked individual from selected ones
    """
    # Select tournament_size individuals at random (no repetition)
    tournament = sample(population.individuals, tournament_size)
    ranked_tournament = rank_population(tournament)

    return ranked_tournament[0][0]


def roulette_wheel_selection(population: Population) -> Individual:
    """
    Select an individual from the population using the roulette wheel selection method.

    Parameters:
    population (Population): population from which to pick an individual.

    Returns:
    Individual: selected individual
    """
    total_fitness = sum([1/i.fitness for i in population]) # get total fitness
    r = uniform(0, total_fitness) # get random number between 0 and total fitness
    position = 0 # initialize position
    for individual in population: # for each individual in population
        position += individual.fitness # add individual fitness to position
        if position > r:
            return individual