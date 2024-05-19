from library.board import Board
from random import random
from operator import attrgetter


def create_generation(population_size, initial_values):
    individuals = []
    for _ in range(population_size):
        individuals.append(Board(values=initial_values).random_fill_with_valid_blocks())
    return individuals


class Population:
    def __init__(
        self, initial_values: list, population_size: int, optimization_type: str
    ):
        # population size
        self.population_size = population_size

        # "min" or "max"
        self.optimization_type = optimization_type

        # individuals in the population
        self.individuals = []

        self.individuals = create_generation(population_size, initial_values)

        print("Population created")

    def evolve(self, generations, selection, xo_prob, xo, mut_prob, elitism=False):
        for generation in range(generations):
            new_population = []

            if elitism:
                if self.optimization_type == "max":
                    elite = max(self, key=attrgetter("fitness"))
                elif self.optimization_type == "min":
                    elite = min(self, key=attrgetter("fitness"))

            while len(new_population) < self.population_size:
                parent_1, parent_2 = selection(self), selection(self)

                if random() < xo_prob:
                    offspring_1, offspring_2 = xo(parent_1, parent_2)
                else:
                    offspring_1, offspring_2 = parent_1, parent_2

                current_individuals_list = [
                    parent_1,
                    parent_2,
                    offspring_1,
                    offspring_2,
                ]
                # get 2 with best fitness from both parents and offsprings
                best_1 = max(current_individuals_list, key=attrgetter("fitness"))
                current_individuals_list.remove(best_1)
                best_2 = max(current_individuals_list, key=attrgetter("fitness"))
                offspring_1, offspring_2 = best_1, best_2

                if random() < mut_prob:
                    offspring_1 = offspring_1.swap_mutation(5)
                if random() < mut_prob:
                    offspring_2 = offspring_2.swap_mutation(5)

                new_population.append(offspring_1)
                if len(new_population) < self.population_size:
                    new_population.append(offspring_2)

            if elitism:
                if self.optimization_type == "max":
                    worst = min(new_population, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_population.append(elite)
                        new_population.remove(worst)
                elif self.optimization_type == "min":
                    worst = max(new_population, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_population.append(elite)
                        new_population.remove(worst)

            self.individuals = new_population

            if self.optimization_type == "max":
                best = max(self, key=attrgetter("fitness"))
            elif self.optimization_type == "min":
                best = min(self, key=attrgetter("fitness"))

            print(
                f"Best individual of gen #{generation + 1} (fitness = {best.fitness}): \n{best}"
            )

            if best.fitness == 0:
                break

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
