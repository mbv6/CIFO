from classes.individual import Individual


def rank_population(population: "list[Individual]") -> "list[tuple[Individual, float]]":
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


def create_generation(population_size: int, **kwargs: dict) -> "list[Individual]":
    """
    Create a generation of individuals with random valid blocks

    Parameters:
    population_size (int): number of individuals in the population
    kwargs[values] (list): list of 81 integers representing the board
    kwargs[blocks] (list): list of 9 lists of 9 integers (blocks) representing the board

    Raises:
    ValueError: if neither 'values' nor 'blocks' are provided

    Returns:
    list[Individual]: list of individuals - the new generation
    """
    individuals = []
    for _ in range(population_size):
        if "values" in kwargs:
            individual = Individual(
                values=kwargs["values"]
            ).random_fill_with_valid_rows()
        elif "blocks" in kwargs:
            individual = Individual(
                blocks=kwargs["blocks"]
            ).random_fill_with_valid_rows()
        else:
            raise ValueError("Either 'values' or 'blocks' must be provided")
        individuals.append(individual)
    return individuals
