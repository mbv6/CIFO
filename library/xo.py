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

def two_point_crossover(
        parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    point1, point2 = sorted([random.randint(1, 8) for _ in range(2)])

    child1_blocks = parent1.blocks[:point1] + parent2.blocks[point1:point2] + parent1.blocks[point2:]
    child2_blocks = parent2.blocks[:point1] + parent1.blocks[point1:point2] + parent2.blocks[point2:]

    child1 = Individual(blocks=child1_blocks)
    child2 = Individual(blocks=child2_blocks)

    return child1, child2


if __name__ == "__main__":
    parent1 = Individual(values=INITIAL_VALUES)
    parent2 = Individual(["." for _ in range(81)])

    child1, child2 = single_point_xo(parent1, parent2)
    print(child1)
    print("\n\n\n----------------\n\n\n")
    print(child2)
