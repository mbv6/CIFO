import math
from functools import reduce


class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self):
        return True

    def is_solved(self):
        return True

    def solve(self):
        return self.board

    def get_row(self, row):
        return self.board[row]

    def get_col(self, col):
        return [row[col] for row in self.board]

    def get_block(self, row, col):
        row_range_min = math.floor(row / 3) * 3
        row_range_max = math.ceil((row + 1) / 3) * 3
        col_range_min = math.floor(col / 3) * 3
        col_range_max = math.ceil((col + 1) / 3) * 3

        return [
            item
            for sublist in [
                [
                    self.board[row_num][col_num]
                    for col_num in range(col_range_min, col_range_max)
                ]
                for row_num in range(row_range_min, row_range_max)
            ]
            for item in sublist
        ]

    def is_number_valid(self, row, col, value):
        return self.board[row][col] == None and value not in self.get_row(
            row
        ) + self.get_col(col) + list(
            reduce(lambda x, y: x + y, self.get_block(row, col), [])
        )

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.board)


if __name__ == "__main__":
    board = [
        [9, None, None, 8, 3, None, 1, 5, 7],
        [5, None, 3, 1, None, 6, 2, 8, None],
        [1, None, None, 7, 4, None, None, 9, None],
        [None, None, None, None, 5, None, 8, 3],
        [3, None, 1, None, None, 4, 6, 7, 2],
        [2, None, None, None, 1, 3, None, None, 9],
        [None, None, 2, None, 7, None, None, 1, None],
        [None, None, None, None, None, None, None, 6, None],
        [None, 3, 4, None, 6, None, 9, 2, None],
    ]

    board_solution = [
        [9, 4, 6, 8, 3, 2, 1, 5, 7],
        [5, 7, 3, 1, 9, 6, 2, 8, 4],
        [1, 2, 8, 7, 4, 5, 3, 9, 6],
        [4, 6, 9, 2, 5, 7, 8, 3, 1],
        [3, 5, 1, 9, 8, 4, 6, 7, 2],
        [2, 8, 7, 6, 1, 3, 5, 4, 9],
        [6, 9, 2, 3, 7, 8, 4, 1, 5],
        [8, 1, 5, 4, 2, 9, 7, 6, 3],
        [7, 3, 4, 5, 6, 1, 9, 2, 8],
    ]

    sudoku = Sudoku(board)

    print(sudoku)
