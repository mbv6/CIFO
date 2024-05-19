def get_row_from_block_id_and_position(block_id, position):
    return (3 * (block_id // 3)) + (position // 3)


def get_col_from_block_id_and_position(block_id, position):
    return (3 * (block_id % 3)) + (position % 3)
