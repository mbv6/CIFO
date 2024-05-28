from copy import deepcopy, copy
from operator import attrgetter
from library.individual import Individual
from random import random

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
            ).random_fill_with_valid_blocks()
        elif "blocks" in kwargs:
            individual = Individual(
                blocks=kwargs["blocks"]
            ).random_fill_with_valid_blocks()
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

        self.individuals = []

        self.individuals = create_generation(population_size, values=initial_values)

        print("Population created")

    def evolve(
        self,
        generations: int,
        selection: object,
        xo: object,
        xo_prob: int,
        mut_prob: int,
        elitism: bool = True,
        elite_len= int,

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
        """
        best = None
        previous_best = (None, float("inf"))
        rank_population(self)
        if elitism:
            self.individuals.sort(key=attrgetter('fitness'), reverse=True)
            elites = []
            for i in range(elite_len):
                elites.append(self.individuals[i])
            elite = copy(min(self.individuals, key=attrgetter('fitness')))

        for generation in range(generations):
            new_population = [best[0]] if best is not None else []
            for i in range(len(self.individuals)):
                self.individuals[i].get_fitness()
            while len(new_population) < self.population_size:
                parent_1, parent_2 = selection(self), selection(self)
                while parent_1 == parent_2:
                    parent_1, parent_2 = selection(self), selection(self)

                if random() < xo_prob:
                    offspring_1, offspring_2 = xo(parent_1, parent_2)
                else:
                    offspring_1, offspring_2 = deepcopy(parent_1), deepcopy(parent_2)

                if random() < mut_prob:
                    offspring_1 = mutation(offspring_1, 5)
                if random() < mut_prob:
                    offspring_2 = mutation(offspring_2, 5)

                new_population.append(offspring_1)
                if len(new_population) < self.population_size:
                    new_population.append(offspring_2)
            if elitism:
                new_population = rank_population(new_population)
                print(new_population)
                for i in range(elite_len):
                    new_population.pop(0)
                new_population.append(elite)

            population_fitness = rank_population(new_population)

            best = min(population_fitness, key=lambda x: x[1])

            if previous_best[1] < best[1]:
                new_population.remove(best[0])
                new_population.append(previous_best[0])
                best = previous_best
            else:
                previous_best = best

            self.individuals = new_population

            print(
                f"Best individual of gen #{generation + 1} (fitness = {best[1]}): \n{best[0]}"
            )

            if best[1] == 0:
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

def rank_population(population: "list[Individual]"):
    """ Rank the population according to the fitness of each individual

    Parameters:
    population (list[Individual]): population to rank

    Returns:
    list[tuple[Individual, float]]: ranked population, sorted from lowest to highest fitness """
    individual_fitness = {}
    for individual in population:
        individual_fitness[individual] = individual.get_fitness()
    return sorted(individual_fitness.items(), key=lambda x: x[1])


