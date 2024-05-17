import numpy as np

class Board:
    HEURISTIC = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [0, 1, 2, 3, 3, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    def __init__(self, size=8):
        self.size = size
        self.board = np.full((self.size, self.size), "-")

    def draw_board(self):
        header = "  " + " ".join(str(i) for i in range(self.size))
        print(header)
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))

    def is_valid_move(self, move):
        x, y = move
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "-"

    def make_move(self, x, y, player):
        if self.is_valid_move((x, y)):
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        self.board[x][y] = "-"

    def get_all_lines(self):
        lines = []
        # Add rows
        for row in self.board:
            lines.append("".join(row))
        # Add columns
        for col in range(self.size):
            lines.append("".join(self.board[:, col]))
        # Add diagonals
        for d in range(-self.size + 1, self.size):
            lines.append("".join(self.board.diagonal(d)))
            lines.append("".join(np.fliplr(self.board).diagonal(d)))
        return lines

    def is_full(self):
        return not np.any(self.board == "-")