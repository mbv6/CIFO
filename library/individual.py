def get_row_from_block_id_and_position(block_id: int, position: int) -> int:
    """
    Get row from block id and position.

    Parameters:
    block_id (int): block id.
    position (int): position.

    Returns:
    int: row.
    """
    return (3 * (block_id // 3)) + (position // 3)


def get_col_from_block_id_and_position(block_id: int, position: int) -> int:
    """
    Get column from block id and position.

    Parameters:
    block_id (int): block id.
    position (int): position.

    Returns:
    int: column.
    """
    return (3 * (block_id % 3)) + (position % 3)
