from classes.individual import Individual
from library.constants import INITIAL_VALUES
from random import randint


def single_point_xo(
    parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    """
    Single point crossover between two individuals.

    Parameters:
    parent1 (Individual): first parent to crossover.
    parent2 (Individual): second parent to crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """
    xo_point = randint(1, 8)

    child1 = Individual(
        blocks=parent1.blocks[:xo_point] + parent2.blocks[xo_point:]
    ).set_fixed(parent1.fixed)
    child2 = Individual(
        blocks=parent2.blocks[:xo_point] + parent1.blocks[xo_point:]
    ).set_fixed(parent2.fixed)

    return child1, child2


def row_single_point_xo(
    parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    """
    Single point crossover between two individuals.

    Parameters:
    parent1 (Individual): first parent to crossover.
    parent2 (Individual): second parent to crossover.

    Returns:
    tuple[Individual, Individual]: two children resulting from the crossover.
    """
    xo_point = randint(1, 8)

    child1 = Individual(
        rows=parent1.rows[:xo_point] + parent2.rows[xo_point:]
    ).set_fixed(parent1.fixed)
    child2 = Individual(
        rows=parent2.rows[:xo_point] + parent1.rows[xo_point:]
    ).set_fixed(parent2.fixed)

    return child1, child2


def uniform_xo(p1: Individual, p2: Individual) -> Individual:
    """Implementation of uniform crossover for Sudoku rows.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individual: Offspring, resulting from the crossover.
    """
    def row_uniform_xo(row1, row2):
        offspring_row1 = [None] * 9
        offspring_row2 = [None] * 9
        available_numbers1 = set(range(1, 10))  # Numbers 1 to 9
        available_numbers2 = set(range(1, 10))  # Numbers 1 to 9

        for i in range(9):
            if uniform(0, 1) < 0.5: # Randomly choose which parent to take the number from
                if row1[i] in available_numbers1:  # If the number is not already in the offspring 1
                    offspring_row1[i] = row1[i]
                    available_numbers1.remove(row1[i])
                if row2[i] in available_numbers2:  # If the number is not already in the offspring 2
                    offspring_row2[i] = row2[i]
                    available_numbers2.remove(row2[i])
            else:
                if row2[i] in available_numbers1:  # If the number is not already in the offspring 1
                    offspring_row1[i] = row2[i]
                    available_numbers1.remove(row2[i])
                if row1[i] in available_numbers2:  # If the number is not already in the offspring 2
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
        offspring_row1, offspring_row2 = uniform_xo(p1.rows[i], p2.rows[i])
        offspring_rows1.append(offspring_row1)
        offspring_rows2.append(offspring_row2)

    offspring1 = Individual(rows=offspring_rows1).set_fixed(p1.fixed)
    offspring2 = Individual(rows=offspring_rows2).set_fixed(p2.fixed)

    return offspring1, offspring2

if __name__ == "__main__":
    parent1 = Individual(values=INITIAL_VALUES)
    parent2 = Individual(["." for _ in range(81)])

    child1, child2 = single_point_xo(parent1, parent2)
    print(child1)
    print("\n\n\n----------------\n\n\n")
    print(child2)
