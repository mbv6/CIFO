def get_row_from_block_id_and_position(block_id: int, position: int) -> int:
    """
    Get row number from block id and position.

    Parameters:
    block_id (int): block id.
    position (int): position.

    Returns:
    int: row.
    """
    return (3 * (block_id // 3)) + (position // 3)


def get_col_from_block_id_and_position(block_id: int, position: int) -> int:
    """
    Get column number from block id and position.

    Parameters:
    block_id (int): block id.
    position (int): position.

    Returns:
    int: column.
    """
    return (3 * (block_id % 3)) + (position % 3)


def get_block_from_row_and_col(row_id: int, col_id: int) -> int:
    """
    Get block number from row and column id.

    Parameters:
    row_id (int): row.
    col_id (int): column.

    Returns:
    int: block.
    """
    return (row_id // 3) * 3 + (col_id // 3)
