from classes.individual import Individual
from random import random
from library.population import rank_population, create_generation
from copy import deepcopy
import pandas as pd


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
        self.initial_values = initial_values
        self.population_size = population_size
        self.individuals = create_generation(population_size, values=initial_values)

        print("Population created")

    def evolve(
        self,
        generations: int,
        selection: object,
        tournament_size: int,
        boltzmann_temperature: int,
        xo: object,
        xo_prob: int,
        mutation: object,
        mut_prob: int,
        generations_without_improvement: int,
        generations_before_reset: int,
        elitism_range: int,
    ) -> pd.DataFrame:
        """
        Run Genetic Algorithm, selecting, crossing and mutating individuals in current generation to create the next one.

        Parameters:
        generations (int): number of generations to be created iteratively
        selection (function): selection function to select individuals from current population to be parents for next generation
        tournament_size (int): number of random individuals to pick from population when using tournament_selection
        boltzmann_temperature (int): controls the level of exploration versus exploitation in the selection process when using boltzmann_selection
        xo (function): cross-over function to create offsprings with selected parents
        xo_prob (int): probability of performing cross-over with selected parents
        mutation (function): mutation function to mutate offsprings
        mut_prob (int): probability of performing mutation on current offsprings
        generations_without_improvement (int): number of generations without improvement
        generations_before_reset (int): number of generations before resetting the population
        elitism_range (int): number of best individuals to keep from one generation to the next
        """
        data = []
        default_mut_prob = mut_prob
        default_xo_prob = xo_prob
        best = None
        top_individuals = []
        no_improvement_counter = 0
        num_mutations = 1
        for generation in range(generations):
            new_population = [individual[0] for individual in top_individuals]

            new_population, num_mutations, mut_prob, xo_prob = self.check_improvement(
                new_population,
                no_improvement_counter,
                generations_without_improvement,
                generations_before_reset,
                default_mut_prob,
                default_xo_prob,
                num_mutations,
                mut_prob,
                xo_prob,
            )

            while len(new_population) < self.population_size:
                parent_1, parent_2 = selection(
                    self, tournament_size, boltzmann_temperature
                ), selection(self, tournament_size, boltzmann_temperature)
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
                [ind for ind, _ in population_fitness[:elitism_range]]
            )[:elitism_range]

            self.individuals = new_population

            if top_individuals[0][0] == best:
                no_improvement_counter += 1
            else:
                no_improvement_counter = 0

            best = top_individuals[0][0]

            data.append([generation + 1, best.fitness])

            print(
                f"Best individual of gen #{generation + 1} (fitness = {best.fitness}): \n{best}"
            )

            if best.fitness == 0:
                print("\n\n\nFOUND FINAL SOLUTION\n\n\n")
                break

        return pd.DataFrame(data, columns=["Generation", "Fitness"])

    def check_improvement(
        self,
        new_population: "list[Individual]",
        no_improvement_counter: int,
        generations_without_improvement: int,
        generations_before_reset: int,
        default_mut_prob: int,
        default_xo_prob: int,
        num_mutations: int,
        mut_prob: int,
        xo_prob: int,
    ) -> "tuple[list[Individual], int, int, int]":
        """
        Check if there is an improvement in the population.

        Parameters:
        new_population (list[Individual]): population of current generation
        no_improvement_counter (int): number of generations without improvement
        generations_without_improvement (int): number of generations without improvement (from parameters)
        generations_before_reset (int): number of generations before resetting the population (from parameters)
        default_mut_prob (int): default mutation probability (from parameters)
        default_xo_prob (int): default cross-over probability (from parameters)
        num_mutations (int): number of mutations
        mut_prob (int): mutation probability
        xo_prob (int): cross-over probability

        Returns:
        list[Individual]: new population
        int: updated number of mutations
        int: updated mutation probability
        int: updated cross-over probability
        """
        if no_improvement_counter >= generations_before_reset:
            new_population = create_generation(
                self.population_size,
                values=self.initial_values,
            )
        elif no_improvement_counter >= generations_without_improvement:
            num_mutations = min(num_mutations + 1, 10)
            mut_prob = min(mut_prob + 0.1, 1)
            xo_prob = max(xo_prob - 0.1, 0)
        else:
            num_mutations = 1
            mut_prob = default_mut_prob
            xo_prob = default_xo_prob

        return new_population, num_mutations, mut_prob, xo_prob

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
