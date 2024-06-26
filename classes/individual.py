from library.constants import EASY_INITIAL_VALUES
from random import randint
from library.individual import (
    get_col_from_block_id_and_position,
    get_row_from_block_id_and_position,
    get_block_from_row_and_col,
)


class Individual:
    """
    Class representing a Sudoku board

    Attributes:
    initial_values (list[string]): list of 81 integers representing the board
    rows (list[list[string]]): list of 9 lists of 9 integers representing the rows of the board
    cols (list[list[string]]): list of 9 lists of 9 integers representing the columns of the board
    blocks (list[list[string]]): list of 9 lists of 9 integers representing the blocks of the board
    fixed (dict[(int, int), int]): dictionary with fixed positions and values
    fitness (int): fitness of the board
    """

    def __init__(self, **kwargs: dict) -> None:
        """
        Initialize the board with either values or blocks

        Parameters:
        values (list[string]): list of 81 integers representing the board
        blocks (list[list[string]]): list of 9 lists of 9 integers (blocks) representing the board
        rows (list[list[string]]): list of 9 lists of 9 integers (rows) representing the board

        Raises:
        ValueError: If values or blocks are not provided
        ValueError: If values has not 81 elements
        ValueError: If blocks has not 9 elements
        """
        self.initial_values = None
        self.rows = [[] for _ in range(9)]
        self.cols = [[] for _ in range(9)]
        self.blocks = [[] for _ in range(9)]
        self.fixed = {}
        self.fitness = None

        if "values" in kwargs and isinstance(kwargs["values"], list):
            if len(kwargs["values"]) != 81:
                raise ValueError("Values must have 81 elements")
            self.initial_setup_with_values(kwargs["values"])
        elif "blocks" in kwargs and isinstance(kwargs["blocks"], list):
            if len(kwargs["blocks"]) != 9:
                raise ValueError("Blocks must have 9 elements")
            self.initial_setup_with_blocks(kwargs["blocks"])
        elif "rows" in kwargs and isinstance(kwargs["rows"], list):
            if len(kwargs["rows"]) != 9:
                raise ValueError("Rows must have 9 elements")
            self.initial_setup_with_rows(kwargs["rows"])
        else:
            raise ValueError(
                "Invalid arguments: One of ['values', 'blocks'] must be provided"
            )

        self.fitness = self.get_fitness()

    def __str__(self) -> str:
        """
        The string representation of the board

        Returns:
        str: string representation of the board
        """

        def value_to_str(value):
            return str(value) if value is not None else "."

        lines = []
        for row_index in range(9):
            if row_index % 3 == 0 and row_index != 0:
                lines.append("- - - - - - - - - - - -")
            row = self.rows[row_index]
            row_str = " ".join(value_to_str(value) for value in row)
            row_with_bars = " | ".join(
                [row_str[i : i + 6] for i in range(0, len(row_str), 6)]
            )
            lines.append(row_with_bars)

        return "\n".join(lines)

    def initial_setup_with_values(self, values: "list[str]") -> "Individual":
        """
        Initialize the board given a list of 81 integers

        Parameters:
        values (list[string]): list of 81 integers representing the board

        Returns:
        Individual: self
        """
        for index in range(81):
            row_index = index // 9
            col_index = index % 9
            block_index = (row_index // 3) * 3 + col_index // 3

            value = values[index]

            self.initial_values = values
            self.rows[row_index].append(value)
            self.cols[col_index].append(value)
            self.blocks[block_index].append(value)

            if value is not None:
                self.fixed[(row_index, col_index)] = value

        return self

    def initial_setup_with_blocks(self, blocks: "list[list[str]]") -> "Individual":
        """
        Initialize the board given a list of 9 lists of 9 integers

        Parameters:
        blocks (list[list[string]]): list of 9 lists of 9 integers (blocks) representing the board

        Returns:
        Individual: self
        """
        self.blocks = blocks
        for block_index, block_values in enumerate(blocks):
            for row_index in range(3):
                for col_index in range(3):
                    position = row_index * 3 + col_index
                    value = block_values[position]
                    row = get_row_from_block_id_and_position(block_index, position)
                    col = get_col_from_block_id_and_position(block_index, position)

                    self.rows[row].append(value)
                    self.cols[col].append(value)

                    if value is not None:
                        self.fixed[(row, col)] = value

        # flatten "rows" list to get initial values
        self.initial_values = [item for row in self.rows for item in row]

        return self

    def initial_setup_with_rows(self, rows: "list[list[str]]") -> "Individual":
        """
        Initialize the board given a list of 9 lists of 9 integers

        Parameters:
        rows (list[list[string]]): list of 9 lists of 9 integers (rows) representing the board

        Returns:
        Individual: self
        """
        self.rows = rows
        for row_index, row_values in enumerate(rows):
            for col_index, value in enumerate(row_values):
                block_index = (row_index // 3) * 3 + col_index // 3
                self.cols[col_index].append(value)
                self.blocks[block_index].append(value)

                if value is not None:
                    self.fixed[(row_index, col_index)] = value

        # flatten "rows" list to get initial values
        self.initial_values = [item for row in self.rows for item in row]

        return self

    def random_fill_with_valid_rows(self) -> "Individual":
        """
        Fill the board with random values in the empty positions of each row

        Returns:
        Individual: self
        """
        for row_index, row_values in enumerate(self.rows):
            missing_values = [i for i in range(1, 10) if i not in row_values]
            for row_value_index in range(len(row_values)):
                if row_values[row_value_index] is None:
                    col_index = row_value_index
                    block_index = get_block_from_row_and_col(row_index, col_index)
                    value = missing_values[randint(0, len(missing_values) - 1)]
                    missing_values.remove(value)
                    self.set_value(row_index, col_index, block_index, value)

        return self

    def random_fill_with_valid_blocks(self) -> "Individual":
        """
        Fill the board with random values in the empty positions of each block

        Returns:
        Individual: self
        """
        for block_index, block_values in enumerate(self.blocks):
            missing_values = [i for i in range(1, 10) if i not in block_values]
            for block_value_index in range(9):
                if block_values[block_value_index] is None:
                    row_index = get_row_from_block_id_and_position(
                        block_index, block_value_index
                    )
                    col_index = get_col_from_block_id_and_position(
                        block_index, block_value_index
                    )
                    value = missing_values[randint(0, len(missing_values) - 1)]
                    missing_values.remove(value)
                    self.set_value(row_index, col_index, block_index, value)

        return self

    def get_value(self, row: int, col: int) -> int:
        """
        Get the value of a position in the board

        Parameters:
        row (int): row index
        col (int): column index

        Returns:
        int: value of the position
        """
        return self.rows[row][col]

    def set_value(self, row: int, col: int, block: int, value: int) -> None:
        """
        Set the value of a position in the board

        Parameters:
        row (int): row index
        col (int): column index
        block (int): block index
        value (int): value to set
        """
        self.rows[row][col] = value
        self.cols[col][row] = value
        self.blocks[block][row % 3 * 3 + col % 3] = value

    def get_fitness(self) -> int:
        """
        Calculate the fitness of the board.

        Currently the fitness is calculated by counting the number of duplicates in columns and blocks.
        There is no need to check for duplicates in rows since when creating "random" boards, we assign already valid rows.

        Returns:
        int: fitness of the board
        """

        # if self.fitness is not None:
        #     return self.fitness

        def duplicate_count(values):
            return len(values) - len(set(values))

        fitness = 0
        for col in self.cols:
            fitness += duplicate_count(col)
        for block in self.blocks:
            fitness += duplicate_count(block)

        self.fitness = fitness

        return fitness

    def get_random_row_position(
        self, row_id: int, disabled_positions: "list[int]" = []
    ) -> "tuple[int, int, int]":
        """
        Get a random non-fixed position in a row.

        Parameters:
        row_id (int): row index
        disabled_positions (list[int]): list of positions to avoid

        Returns:
        int: block position
        int: row index
        int: column index
        """
        col_id = randint(0, 8)
        block_id = None
        is_valid = False

        while not is_valid or (row_id, col_id) in disabled_positions:
            col_id = randint(0, 8)
            block_id = get_block_from_row_and_col(row_id, col_id)
            is_valid = not self.is_position_fixed(row_id, col_id)

        return row_id, col_id, block_id

    def get_random_position(
        self, block_id: int, disabled_positions: "list[(int, int)]" = []
    ) -> "tuple[int, int, int]":
        """
        Get a random non-fixed position in a block.

        Parameters:
        block_id (int): block index
        disabled_positions (list[(int, int)]): list of positions to avoid

        Returns:
        int: block position
        int: row index
        int: column index
        """
        random_block_pos = randint(0, 8)
        row_id = None
        col_id = None
        is_valid = False

        while not is_valid or (row_id, col_id) in disabled_positions:
            random_block_pos = randint(0, 8)
            row_id = get_row_from_block_id_and_position(block_id, random_block_pos)
            col_id = get_col_from_block_id_and_position(block_id, random_block_pos)
            is_valid = not self.is_position_fixed(row_id, col_id)

        return random_block_pos, row_id, col_id

    def is_position_fixed(self, row_id: int, col_id: int) -> bool:
        """
        Check if a position is fixed

        Parameters:
        row_id (int): row index
        col_id (int): column index

        Returns:
        bool: True if the position is fixed, False otherwise
        """
        return (row_id, col_id) in self.fixed

    def set_fixed(self, fixed: "dict[(int, int), int]") -> "Individual":
        """
        Set the fixed positions of the board

        Parameters:
        fixed (dict[(int, int), int]): dictionary with fixed positions and values

        Returns:
        Individual: self
        """
        self.fixed = fixed
        return self
