from random import sample
from operator import attrgetter
from library.population import Population
from library.board import Board


def tournament_selection(population: Population, tournament_size=100) -> Board:
    # Select tournament_size individuals at random (no repetition)
    tournament = sample(population.individuals, tournament_size)
    if population.optimization_type == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optimization_type == "min":
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception(f"Optimization not supported (max/min)")
