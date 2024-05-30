from random import randint
from classes.individual import Individual
from library.individual import get_block_from_row_and_col


def block_swap_mutation(individual: Individual, num_mutations=1) -> Individual:
    """
    Perform a swap mutation in the board

    Parameters:
    individual (Individual): individual to be mutated
    num_mutations (int): number of mutations to perform

    Returns:
    Individual: mutated individual
    """
    for _ in range(num_mutations):
        block_id = randint(0, 8)

        random_pos_1, row_id_1, col_id_1 = individual.get_random_row_position(block_id)
        random_pos_2, row_id_2, col_id_2 = individual.get_random_position(
            block_id, disabled_positions=[random_pos_1]
        )

        selected_block = individual.blocks[block_id]
        val_1 = selected_block[random_pos_1]
        val_2 = selected_block[random_pos_2]

        individual.set_value(row_id_1, col_id_1, block_id, val_2)
        individual.set_value(row_id_2, col_id_2, block_id, val_1)

    return individual


def row_swap_mutation(individual: Individual, num_mutations=1) -> Individual:
    """
    Perform a swap mutation in the board

    Parameters:
    individual (Individual): individual to be mutated
    num_mutations (int): number of mutations to perform

    Returns:
    Individual: mutated individual
    """
    for _ in range(num_mutations):
        row_id = randint(0, 8)

        _, col_id_1, block_id_1 = individual.get_random_row_position(row_id)
        _, col_id_2, block_id_2 = individual.get_random_row_position(
            row_id, disabled_positions=[(row_id, col_id_1)]
        )

        selected_row = individual.rows[row_id]
        val_1 = selected_row[col_id_1]
        val_2 = selected_row[col_id_2]

        individual.set_value(row_id, col_id_1, block_id_1, val_2)
        individual.set_value(row_id, col_id_2, block_id_2, val_1)

    return individual


def row_random_mutation(
    individual: Individual, placeholder_num_mutations=None
) -> Individual:
    """
    Randomize a row in the board, except from the fixed values

    Parameters:
    individual (Individual): individual to be mutated
    placeholder_num_mutations (Any): used to keep same template between all mutation functions

    Returns:
    Individual: mutated individual
    """
    row_id = randint(0, 8)
    new_row = [None for _ in range(9)]
    available_values = []

    for col_id in range(9):
        if individual.is_position_fixed(row_id, col_id):
            new_row[col_id] = individual.get_value(row_id, col_id)
        else:
            available_values.append(individual.get_value(row_id, col_id))

    while None in new_row:
        new_value = available_values.pop(randint(0, len(available_values) - 1))
        new_row[new_row.index(None)] = new_value

    for col_id in range(9):
        individual.set_value(
            row_id, col_id, get_block_from_row_and_col(row_id, col_id), new_row[col_id]
        )

    return individual


def row_inversion_mutation(
    individual: Individual, placeholder_num_mutations=None
) -> Individual:
    """
    Invert the order of all non-fixed values in a row

    Parameters:
    individual (Individual): individual to be mutated
    placeholder_num_mutations (Any): used to keep same template between all mutation functions

    Returns:
    Individual: mutated individual
    """
    row_id = randint(0, 8)
    new_row = [None for _ in range(9)]
    available_values = []

    for col_id in range(9):
        if individual.is_position_fixed(row_id, col_id):
            new_row[col_id] = individual.get_value(row_id, col_id)
        else:
            available_values.append(individual.get_value(row_id, col_id))

    available_values.reverse()

    while None in new_row:
        new_value = available_values.pop(0)
        new_row[new_row.index(None)] = new_value

    for col_id in range(9):
        individual.set_value(
            row_id, col_id, get_block_from_row_and_col(row_id, col_id), new_row[col_id]
        )

    return individual
