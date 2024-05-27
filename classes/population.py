from classes.individual import Individual
from random import random
from library.population import rank_population
from copy import deepcopy


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


class Population:
    """
    Class representing generation (population) of Sudoku boards (Individual)

    Attributes:
    population_size (int): number of individuals in each generation
    individuals (list[Individual]): list of all individuals in current generation
    """

    def __init__(self, initial_values: list, population_size: int):
        """
        Initialize the population.

        Parameters:
        initial_values (list[string]): list of 81 integers representing board to be solved
        population_size (int): number of individuals in each generation
        """
        self.population_size = population_size

        self.individuals = create_generation(population_size, values=initial_values)

        print("Population created")

    def evolve(
        self,
        generations: int,
        selection: object,
        xo: object,
        xo_prob: int,
        mutation: object,
        mut_prob: int,
        generations_without_improvement: int,
        elitism_range: int,
    ):
        """
        Run Genetic Algorithm, selecting, crossing and mutating individuals in current generation to create the next one.

        Parameters:
        generations (int): number of generations to be created iteratively
        selection (function): selection function to select individuals from current population to be parents for next generation
        xo (function): cross-over function to create offsprings with selected parents
        xo_prob (int): probability of performing cross-over with selected parents
        mutation (function): mutation function to mutate offsprings
        mut_prob (int): probability of performing mutation on current offsprings
        generations_without_improvement (int): number of generations without improvement
        elitism_range (int): number of best individuals to keep from one generation to the next
        """
        top_individuals = []
        num_mutations = 1
        for generation in range(generations):
            new_population = [individual[0] for individual in top_individuals]

            while len(new_population) < self.population_size:
                parent_1, parent_2 = selection(self), selection(self)
                # check if parents aren't the same
                while parent_1 == parent_2:
                    parent_1, parent_2 = selection(self), selection(self)

                if random() < xo_prob:
                    offspring_1, offspring_2 = xo(parent_1, parent_2)
                else:
                    offspring_1, offspring_2 = deepcopy(parent_1), deepcopy(parent_2)

                current_individuals_list = [
                    parent_1,
                    parent_2,
                    offspring_1,
                    offspring_2,
                ]
                # get 2 with best fitness from both parents and offsprings
                best_values = rank_population(current_individuals_list)[:2]

                offspring_1, offspring_2 = deepcopy(best_values[0][0]), deepcopy(
                    best_values[1][0]
                )

                if random() < mut_prob:
                    offspring_1 = mutation(offspring_1, num_mutations)
                if random() < mut_prob:
                    offspring_2 = mutation(offspring_2, num_mutations)

                new_population.append(offspring_1)
                if len(new_population) < self.population_size:
                    new_population.append(offspring_2)

            population_fitness = rank_population(new_population)

            top_individuals = rank_population(
                list(
                    map(
                        lambda x: x[0],
                        top_individuals + population_fitness[:elitism_range],
                    )
                )
            )[:elitism_range]

            self.individuals = new_population

            best = top_individuals[0][1]

            print(
                f"Best individual of gen #{generation + 1} (fitness = {new_population[0].fitness}): \n{new_population[0]}"
            )

            if top_individuals[0][1] == 0:
                break

    def __len__(self) -> int:
        """
        Length of class.

        Returns:
        int: Length of individuals attribute.
        """
        return len(self.individuals)

    def __getitem__(self, position: int) -> Individual:
        """
        Get item from class.

        Parameters:
        position (int): index of individual to be retrieved.

        Returns:
        Individual: element at index = position in individuals attribute.
        """
        return self.individuals[position]
