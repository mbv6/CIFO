from individual import Individual


def rank_population(population: "list[Individual]"):
    """
    Rank the population according to the fitness of each individual

    Parameters:
    population (list[Individual]): population to rank

    Returns:
    list[tuple[Individual, float]]: ranked population, sorted from lowest to highest fitness
    """
    individual_fitness = {}
    for individual in population:
        individual_fitness[individual] = individual.get_fitness()
    return sorted(individual_fitness.items(), key=lambda x: x[1])
