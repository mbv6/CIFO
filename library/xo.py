from classes.individual import Individual
from library.constants import INITIAL_VALUES
from random import randint, sample, uniform


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

def blocks_two_point_crossover(
        parent1: Individual, parent2: Individual
) -> "tuple[Individual, Individual]":
    point1, point2 = sorted([random.randint(1, 8) for _ in range(2)])

    child1_blocks = parent1.blocks[:point1] + parent2.blocks[point1:point2] + parent1.blocks[point2:] # child1 gets the blocks from parent1 before point1, the blocks from parent2 between point1 and point2, and the blocks from parent1 after point2
    child2_blocks = parent2.blocks[:point1] + parent1.blocks[point1:point2] + parent2.blocks[point2:] # child2 gets the blocks from parent2 before point1, the blocks from parent1 between point1 and point2, and the blocks from parent2 after point2

    child1 = Individual(blocks=child1_blocks)
    child2 = Individual(blocks=child2_blocks)

    return child1, child2

def cycle_xo(parent1, parent2):
    """Implementation of cycle crossover for Sudoku.

    Args:
        parent1 (Individual): First parent (Sudoku individual).
        parent2 (Individual): Second parent (Sudoku individual).

    Returns:
        Individual, Individual: Two offspring Sudoku individuals resulting from the crossover.
    """
    def cycle_xo_row(row1, row2):
        o1 = [None] * 9
        o2 = [None] * 9
        visited = [False] * 9

        while None in o1:
            index = o1.index(None)
            cycle_start = index
            val1 = row1[index]

            while not visited[index]:
                o1[index] = row1[index]
                o2[index] = row2[index]
                visited[index] = True

                val2 = row2[index]
                index = row1.index(val2)
                if row1[index] == val1:  # Handle duplicates by breaking the cycle
                    break

            # copy the cycle elements
            while val1 != val2:
                o1[index] = row1[index]
                o2[index] = row2[index]
                val2 = row2[index]
                index = row1.index(val2)

            # copy the rest
            for i in range(9):
                if o1[i] is None:
                    o1[i] = row2[i]
                    o2[i] = row1[i]

        return o1, o2

    offspring1 = [[None] * 9 for _ in range(9)]
    offspring2 = [[None] * 9 for _ in range(9)]

    for i in range(9):
        offspring1[i], offspring2[i] = cycle_xo_row(parent1.rows[i], parent2.rows[i])

    # Create Individual objects for the offspring
    child1 = Individual(rows=offspring1).set_fixed(parent1.fixed)
    child2 = Individual(rows=offspring2).set_fixed(parent2.fixed)

    return child1, child2

def rows_uniform_xo(p1: Individual, p2: Individual) -> Individual:
    """Implementation of uniform crossover for Sudoku rows.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individual: Offspring, resulting from the crossover.
    """
    def uniform_crossover_row(row1, row2):
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
        offspring_row1, offspring_row2 = uniform_crossover_row(p1.rows[i], p2.rows[i])
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
