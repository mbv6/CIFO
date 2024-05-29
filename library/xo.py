from classes.individual import Individual
from library.constants import EASY_INITIAL_VALUES
from random import randint, sample, random


def block_single_point_xo(
    parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    """
    Single point crossover between blocks of two individuals.

    Parameters:
    parent1 (Individual): first parent to crossover.
    parent2 (Individual): second parent to crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """
    xo_point = randint(1, 8)

    child1, child2 = Individual(
        blocks=parent1.blocks[:xo_point] + parent2.blocks[xo_point:]
    ).set_fixed(parent1.fixed), Individual(
        blocks=parent2.blocks[:xo_point] + parent1.blocks[xo_point:]
    ).set_fixed(
        parent2.fixed
    )

    return child1, child2


def row_single_point_xo(
    parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    """
    Single point crossover between rows of two individuals.

    Parameters:
    parent1 (Individual): first parent to crossover.
    parent2 (Individual): second parent to crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """
    xo_point = randint(1, 8)

    child1, child2 = Individual(
        rows=parent1.rows[:xo_point] + parent2.rows[xo_point:]
    ).set_fixed(parent1.fixed), Individual(
        rows=parent2.rows[:xo_point] + parent1.rows[xo_point:]
    ).set_fixed(
        parent2.fixed
    )

    return child1, child2


def row_partially_mapped_xo(
    parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    """
    Partially mapped crossover between rows two individuals.

    Parameters:
    parent1 (Individual): first parent to crossover.
    parent2 (Individual): second parent to crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """

    def pmx_single(row1, row2):
        size = len(row1)
        child1_rows, child2_rows = [-1] * size, [-1] * size
        crossover_points = sorted(sample(range(size), 2))
        child1_rows[crossover_points[0] : crossover_points[1]] = row2[
            crossover_points[0] : crossover_points[1]
        ]
        child2_rows[crossover_points[0] : crossover_points[1]] = row1[
            crossover_points[0] : crossover_points[1]
        ]

        def fill_pmx(child, parent):
            for i in range(size):
                if child[i] == -1:
                    candidate = parent[i]
                    while candidate in child:
                        candidate = parent[child.index(candidate)]
                    child[i] = candidate
            return child

        return fill_pmx(child1_rows, row1), fill_pmx(child2_rows, row2)

    child1_rows, child2_rows = [], []
    for r1, r2 in zip(parent1.rows, parent2.rows):
        c1, c2 = pmx_single(r1, r2)
        child1_rows.append(c1)
        child2_rows.append(c2)

    child1, child2 = Individual(rows=child1_rows).set_fixed(parent1.fixed), Individual(
        rows=child2_rows
    ).set_fixed(parent2.fixed)

    return child1, child2


def row_uniform_xo(p1: Individual, p2: Individual) -> Individual:
    """Implementation of uniform crossover for Sudoku rows.

    Parameters:
    p1 (Individual): First parent for crossover.
    p2 (Individual): Second parent for crossover.

    Returns:
    Individual: Offspring, resulting from the crossover.
    """

    def uniform_single(row1, row2):
        offspring_row1 = [None] * 9
        offspring_row2 = [None] * 9
        available_numbers1 = [i for i in range(1, 10)]  # Numbers 1 to 9
        available_numbers2 = [i for i in range(1, 10)]  # Numbers 1 to 9

        for i in range(9):
            if random() < 0.5:  # Randomly choose which parent to take the number from
                if (
                    row1[i] in available_numbers1
                ):  # If the number is not already in the offspring 1
                    offspring_row1[i] = row1[i]
                    available_numbers1.remove(row1[i])
                if (
                    row2[i] in available_numbers2
                ):  # If the number is not already in the offspring 2
                    offspring_row2[i] = row2[i]
                    available_numbers2.remove(row2[i])
            else:
                if (
                    row2[i] in available_numbers1
                ):  # If the number is not already in the offspring 1
                    offspring_row1[i] = row2[i]
                    available_numbers1.remove(row2[i])
                if (
                    row1[i] in available_numbers2
                ):  # If the number is not already in the offspring 2
                    offspring_row2[i] = row1[i]
                    available_numbers2.remove(row1[i])

        # Fill in the remaining slots with available numbers
        for i in range(9):
            if offspring_row1[i] is None:
                offspring_row1[i] = available_numbers1.pop()
            if offspring_row2[i] is None:
                offspring_row2[i] = available_numbers2.pop()

        return offspring_row1, offspring_row2

    offspring_rows1 = []
    offspring_rows2 = []

    for i in range(9):
        offspring_row1, offspring_row2 = uniform_single(p1.rows[i], p2.rows[i])
        offspring_rows1.append(offspring_row1)
        offspring_rows2.append(offspring_row2)

    offspring1 = Individual(rows=offspring_rows1).set_fixed(p1.fixed)
    offspring2 = Individual(rows=offspring_rows2).set_fixed(p2.fixed)

    return offspring1, offspring2


if __name__ == "__main__":
    parent1 = Individual(values=EASY_INITIAL_VALUES)
    parent2 = Individual(["." for _ in range(81)])

    child1, child2 = block_single_point_xo(parent1, parent2)
    print(child1)
    print("\n\n\n----------------\n\n\n")
    print(child2)
