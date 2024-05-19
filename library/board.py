from library.constants import INITIAL_VALUES
from random import randint
from library.utils import (
    get_col_from_block_id_and_position,
    get_row_from_block_id_and_position,
)


class Board:
    def __init__(self, values=None, blocks=None):
        if values is None and blocks is None:
            raise ValueError("Either values or blocks must be provided")
        elif values is not None and blocks is not None:
            raise ValueError("Only one of values or blocks must be provided")

        self.initial_values = None
        self.rows = [[] for _ in range(9)]
        self.cols = [[] for _ in range(9)]
        self.blocks = [[] for _ in range(9)]
        self.fixed = {}
        self.fitness = None

        if values is not None:
            self.initial_setup_with_values(values)
        elif blocks is not None:
            self.initial_setup_with_blocks(blocks)
        else:
            raise ValueError("Something unexpected happened")

    def __str__(self):
        def value_to_str(value):
            return str(value) if value is not None else "."

        def row_to_str(row):
            return " ".join(value_to_str(value) for value in row)

        return "\n".join(row_to_str(self.rows[row_index]) for row_index in range(9))

    def initial_setup_with_values(self, values):
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

        self.fitness = self.get_fitness()

        return self

    def initial_setup_with_blocks(self, blocks):
        self.blocks = blocks
        for block_index, block_values in enumerate(blocks):
            for row_index in range(3):
                for col_index in range(3):
                    value = block_values[row_index * 3 + col_index]
                    row = block_index // 3 * 3 + row_index
                    col = block_index % 3 * 3 + col_index

                    self.rows[row].append(value)
                    self.cols[col].append(value)

                    if value is not None:
                        self.fixed[(row, col)] = value

        # flatten "rows" list to get initial values
        self.initial_values = [item for row in self.rows for item in row]

        self.fitness = self.get_fitness()

        return self

    def random_fill_with_valid_blocks(self):
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

        self.fitness = None
        self.fitness = self.get_fitness()

        return self

    def get_value(self, row, col):
        return self.rows[row][col]

    def set_value(self, row, col, block, value):
        self.rows[row][col] = value
        self.cols[col][row] = value
        self.blocks[block][row % 3 * 3 + col % 3] = value

    def get_fitness(self):
        def duplicate_count(values):
            return len(values) - len(set(values))

        # we create "random" boards with already valid blocks so no need to check for duplicates in blocks
        self.fitness = 0
        for row in self.rows:
            self.fitness += duplicate_count(row)
        for col in self.cols:
            self.fitness += duplicate_count(col)

        return self.fitness

    def swap_mutation(self, num_mutations=1):
        for _ in range(num_mutations):
            block_id = randint(0, 8)

            random_pos_1, row_id_1, col_id_1 = self.get_random_position(block_id)
            random_pos_2, row_id_2, col_id_2 = self.get_random_position(
                block_id, disabled_positions=[random_pos_1]
            )

            selected_block = self.blocks[block_id]
            val_1 = selected_block[random_pos_1]
            val_2 = selected_block[random_pos_2]

            self.set_value(row_id_1, col_id_1, block_id, val_2)
            self.set_value(row_id_2, col_id_2, block_id, val_1)

        return self

    def get_random_position(self, block_id, disabled_positions=[]):
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

    def is_position_fixed(self, row_id, col_id):
        return (row_id, col_id) in self.fixed

    def set_fixed(self, fixed):
        self.fixed = fixed

        return self


if __name__ == "__main__":
    board = Board(values=INITIAL_VALUES)

    board2 = board.random_fill_with_valid_blocks()

    print(board2)
