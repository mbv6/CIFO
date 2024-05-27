from random import randint
from classes.individual import Individual


def swap_mutation(individual: Individual, num_mutations=1):
    """
    Perform a swap mutation in the board

    Parameters:
    num_mutations (int): number of mutations to perform

    Returns:
    Individual: Individual
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


def row_swap_mutation(individual: Individual, num_mutations=1):
    """
    Perform a swap mutation in the board

    Parameters:
    num_mutations (int): number of mutations to perform

    Returns:
    Individual: Individual
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
