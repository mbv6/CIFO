from classes.individual import Individual
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


def row_uniform_xo(p1: Individual, p2: Individual) -> "tuple[Individual, Individual]":
    """
    Implementation of uniform crossover for Sudoku rows.

    Parameters:
    p1 (Individual): First parent for crossover.
    p2 (Individual): Second parent for crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """

    def uniform_single(row1, row2):
        child1_row = [None] * 9
        child2_row = [None] * 9
        available_numbers1 = [i for i in range(1, 10)]  # Numbers 1 to 9
        available_numbers2 = [i for i in range(1, 10)]  # Numbers 1 to 9

        for i in range(9):
            if random() < 0.5:  # Randomly choose which parent to take the number from
                if (
                    row1[i] in available_numbers1
                ):  # If the number is not already in the child 1
                    child1_row[i] = row1[i]
                    available_numbers1.remove(row1[i])
                if (
                    row2[i] in available_numbers2
                ):  # If the number is not already in the child 2
                    child2_row[i] = row2[i]
                    available_numbers2.remove(row2[i])
            else:
                if (
                    row2[i] in available_numbers1
                ):  # If the number is not already in the child 1
                    child1_row[i] = row2[i]
                    available_numbers1.remove(row2[i])
                if (
                    row1[i] in available_numbers2
                ):  # If the number is not already in the child 2
                    child2_row[i] = row1[i]
                    available_numbers2.remove(row1[i])

        # Fill in the remaining slots with available numbers
        for i in range(9):
            if child1_row[i] is None:
                child1_row[i] = available_numbers1.pop()
            if child2_row[i] is None:
                child2_row[i] = available_numbers2.pop()

        return child1_row, child2_row

    child1_rows = []
    child2_rows = []

    for i in range(9):
        child1_row, child2_row = uniform_single(p1.rows[i], p2.rows[i])
        child1_rows.append(child1_row)
        child2_rows.append(child2_row)

    child1 = Individual(rows=child1_rows).set_fixed(p1.fixed)
    child2 = Individual(rows=child2_rows).set_fixed(p2.fixed)

    return child1, child2
