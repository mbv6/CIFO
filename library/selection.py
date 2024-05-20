from random import sample
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
