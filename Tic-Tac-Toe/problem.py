import os
import time
from collections import defaultdict

import numpy as np


class Problem:
    def __init__(self):
        self.size = 8
        self.board = np.full((self.size, self.size), "·")
        self.player_turn = "x"

    def draw_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(str(i) + " " + " ".join(self.board[i]))

    def is_goal(self):
        return any(self.check_winner(player) for player in ["x", "o"])

    def is_valid_move(self, x, y):
        return (
            x >= 0
            and x < self.size
            and y >= 0
            and y < self.size
            and self.board[x, y] == "·"
        )

    def place_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x, y] = player
            return True
        return False

    def undo_move(self, x, y):
        self.board[x, y] = "·"

    def check_winner(self, player):
        # Check rows, columns, and diagonals for a win condition
        for d in range(-self.size + 1, self.size):
            # Check diagonals
            diag1 = [
                self.board[i, i + d]
                for i in range(self.size)
                if 0 <= i < self.size and 0 <= i + d < self.size
            ]
            diag2 = [
                self.board[i, d + i]
                for i in range(self.size)
                if 0 <= i < self.size and 0 <= d + i < self.size
            ]
            if self.line_winner(diag1, player) or self.line_winner(diag2, player):
                return True
        # Check rows and columns
        for i in range(self.size):
            row = self.board[i, :]
            col = self.board[:, i]
            if self.line_winner(row, player) or self.line_winner(col, player):
                return True
        return False

    def line_winner(self, line, player):
        # Check if there are four consecutive player tokens in a line
        count = 0
        for cell in line:
            if cell == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def get_possible_moves(self):
        return [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.board[x, y] == "·"
        ]


class SearchStrategy:
    def alpha_beta_search(
        self,
        problem,
        depth,
        alpha=-float("inf"),
        beta=float("inf"),
        maximizing_player=True,
    ):
        if depth == 0 or problem.is_goal():
            return self.evaluate(problem), None

        if maximizing_player:
            max_eval = -float("inf")
            best_move = None
            for x, y in problem.get_possible_moves():
                problem.place_move(x, y, "x")
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(x, y)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for x, y in problem.get_possible_moves():
                problem.place_move(x, y, "o")
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(x, y)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, problem):
        score = 0
        player, opponent = ("X", "O") if problem.player_turn == "X" else ("O", "X")

        lines = []
        # Same as check_winner but used for scoring
        for i in range(problem.size):
            lines.append(problem.board[i, :])
            lines.append(problem.board[:, i])

        for d in range(-problem.size + 4, problem.size - 3):
            lines.append(np.diagonal(problem.board, offset=d))
            lines.append(np.diagonal(np.fliplr(problem.board), offset=d))

        for line in lines:
            line_str = "".join(line)
            score += line_str.count(player * 4) * 100
            score -= line_str.count(opponent * 4) * 100
            score += line_str.count(player * 3 + "·") * 10
            score -= line_str.count(opponent * 3 + "·") * 10
            score += line_str.count("·" + player * 3) * 10
            score -= line_str.count("·" + opponent * 3) * 10

        return score


# Main game loop
def play_game():
    problem = Problem()  # Using the modified Problem class with 8x8 board
    strategy = SearchStrategy()
    while not problem.is_goal() and any(problem.board.flatten() == "·"):
        problem.draw_board()
        if problem.player_turn == "x":  # AI plays as 'x'
            print("AI is thinking...")
            _, move = strategy.alpha_beta_search(
                problem, depth=3
            )  # Using Alpha Beta with depth=3
            if move:
                problem.place_move(*move, "x")
            problem.player_turn = "o"
        else:  # Human plays as 'o'
            move = tuple(map(int, input("Enter your move (row col): ").split()))
            while not problem.place_move(*move, "o"):
                print("Invalid move, try again.")
                move = tuple(map(int, input("Enter your move (row col): ").split()))
            problem.player_turn = "x"

        os.system(
            "cls" if os.name == "nt" else "clear"
        )  # Clear the console to redraw the board cleanly

    problem.draw_board()
    if problem.check_winner("x"):
        print("AI wins!")
    elif problem.check_winner("o"):
        print("Player wins!")
    else:
        print("It's a draw!")


play_game()

p = Problem()
s = SearchStrategy()

# start = time.time()
# move = s.alpha_beta_search(p)
# print(move)
# print("Time:", time.time() - start)
