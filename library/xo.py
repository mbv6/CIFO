from classes.individual import Individual
from library.constants import INITIAL_VALUES
from random import randint, sample


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

def pmx(p1: Individual, p2: Individual) -> "tuple[Individual, Individual]":
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(9), 2)
    xo_points.sort()
    def pmx_offspring(row1, row2):

        o = [None] * 9
        # offspring2
        o[xo_points[0]:xo_points[1]]  = row1[xo_points[0]:xo_points[1]]
        z = set(row2[xo_points[0]:xo_points[1]]) - set(row1[xo_points[0]:xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = row2.index(row1[row2.index(temp)])
            while o[index] is not None:
                temp = index
                index = row2.index(row1[temp])
            o[index] = i

        # numbers that doesn't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = row2[index]
        return o

    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2

if __name__ == "__main__":
    parent1 = Individual(values=INITIAL_VALUES)
    parent2 = Individual(["." for _ in range(81)])

    child1, child2 = single_point_xo(parent1, parent2)
    print(child1)
    print("\n\n\n----------------\n\n\n")
    print(child2)
