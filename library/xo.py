from library.board import Board
from library.constants import INITIAL_VALUES
from random import randint


def single_point_xo(parent1: Board, parent2: Board) -> "tuple[Board, Board]":
    # single point crossover
    xo_point = randint(1, 8)

    child1 = Board(
        blocks=parent1.blocks[:xo_point] + parent2.blocks[xo_point:]
    ).set_fixed(parent1.fixed)
    child2 = Board(
        blocks=parent2.blocks[:xo_point] + parent1.blocks[xo_point:]
    ).set_fixed(parent2.fixed)

    return child1, child2


if __name__ == "__main__":
    parent1 = Board(values=INITIAL_VALUES)
    parent2 = Board(["." for _ in range(81)])

    child1, child2 = single_point_xo(parent1, parent2)
    print(child1)
    print("\n\n\n----------------\n\n\n")
    print(child2)
