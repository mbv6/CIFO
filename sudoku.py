class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self):
        return True

    def is_solved(self):
        return True

    def solve(self):
        return self.board

    def get_block(self, row, col):
        if row < 3:
            if col < 3:
                return [[self.board[j][i] for i in range(3)] for j in range(3)]
            elif col < 6:
                return [self.board[i][j] for i in range(3) for j in range(3, 6)]
            else:
                return [self.board[i][j] for i in range(3) for j in range(6, 9)]
        elif row < 6:
            if col < 3:
                return [self.board[i][j] for i in range(3, 6) for j in range(3)]
            elif col < 6:
                return [self.board[i][j] for i in range(3, 6) for j in range(3, 6)]
            else:
                return [self.board[i][j] for i in range(3, 6) for j in range(6, 9)]
        elif row < 9:
            if col < 3:
                return [self.board[i][j] for i in range(6, 9) for j in range(3)]
            elif col < 6:
                return [self.board[i][j] for i in range(6, 9) for j in range(3, 6)]
            else:
                return [self.board[i][j] for i in range(6, 9) for j in range(6, 9)]
        else:
            return None

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
