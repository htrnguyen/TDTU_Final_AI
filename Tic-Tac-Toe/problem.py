import numpy as np


class Problem:
    def __init__(self):
        self.board = np.full((8, 8), " ")
        self.player_turn = "X"  # X always starts

    def draw_board(self):
        for row in range(len(self.board)):
            if row != 0:
                print("—" * (8 * 4 - 2))
            print(" | ".join(self.board[row]))

    def is_valid_move(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == " "

    def place_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.player_turn
            self.player_turn = "O" if self.player_turn == "X" else "X"

    def check_winner(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != " ":
                    current = self.board[row][col]
                    for d in directions:
                        win = True

                        for i in range(1, 4):
                            r, c = row + d[0] * i, col + d[1] * i
                            if not (
                                0 <= r < 8
                                and 0 <= c < 8
                                and self.board[r][c] == current
                            ):
                                win = False
                                break
                        if win:
                            return current
        return None

    def game_over(self):
        return self.check_winner() is not None or np.all(self.board != " ")

    def get_state(self):
        return self.board, self.player_turn

    def get_possible_moves(self):
        return [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(r, c)]

    def utility(self):
        winner = self.check_winner()
        if winner == "X":
            return 1
        elif winner == "O":
            return -1
        else:
            return 0

    def actions(self):
        return self.get_possible_moves()

    def result(self, state, action):
        new_board = np.copy(state[0])
        new_board[action[0], action[1]] = self.player_turn
        return new_board, "O" if self.player_turn == "X" else "X"
