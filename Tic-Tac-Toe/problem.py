import os
import time
from collections import defaultdict

import numpy as np


class Problem:
    def __init__(self):
        self.size = 5
        self.board = np.full((self.size, self.size), "·")
        self.player_turn = "o"
        self.transposition_table = defaultdict(lambda: (None, None))

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
        valid = self.is_valid_move(x, y)
        if valid:
            self.board[x, y] = player
        return valid

    def undo_move(self, x, y):
        self.board[x, y] = "·"

    def check_winner(self, player):
        lines = []
        for d in range(-self.size, self.size):
            lines.append(
                [
                    self.board[i, i + d]
                    for i in range(self.size)
                    if 0 <= i < self.size and 0 <= i + d < self.size
                ]
            )
            lines.append(
                [
                    self.board[i + d, i]
                    for i in range(self.size)
                    if 0 <= i < self.size and 0 <= i + d < self.size
                ]
            )

        for x in range(self.size):
            lines.append(list(self.board[x, :]))
            lines.append(list(self.board[:, x]))

        for line in lines:
            for i in range(len(line) - 3):
                if all(line[i + j] == player for j in range(4)):
                    return True
        return False

    def get_possible_moves(self):
        return [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.board[x, y] == "·"
        ]


class SearchStrategy:
    def __init__(self):
        self.transposition_table = {}

    def evaluate_board(self, board):
        score = 0
        # Example scoring: favor central positions
        center = len(board) // 2
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x, y] == "x":
                    score += 1 - (abs(x - center) + abs(y - center)) / center
                elif board[x, y] == "o":
                    score -= 1 - (abs(x - center) + abs(y - center)) / center
        return score

    def alpha_beta_search(self, problem, depth, alpha, beta, maximizing_player):
        state_key = (tuple(map(tuple, problem.board)), maximizing_player, depth)
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]
        if depth == 0 or problem.is_goal():
            score = self.evaluate_board(problem.board)
            return score, None
        best_move = None
        moves = problem.get_possible_moves()
        if maximizing_player:
            max_eval = float("-inf")
            for move in moves:
                problem.place_move(*move, problem.player_turn)
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(*move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = (max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for move in moves:
                problem.place_move(*move, problem.player_turn)
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            self.transposition_table[state_key] = (min_eval, best_move)
            return min_eval, best_move


def iterative_deepening(problem, strategy, max_depth, timeout):
    best_move = None
    best_eval = float("-inf")
    start_time = time.time()
    for depth in range(1, max_depth + 1):
        eval, move = strategy.alpha_beta_search(
            problem, depth, float("-inf"), float("inf"), True
        )
        if eval > best_eval:
            best_eval = eval
            best_move = move
        if time.time() - start_time > timeout:
            break
    return best_move


# Main
def play_game():
    problem = Problem()
    strategy = SearchStrategy()
    while not problem.is_goal() and any(problem.board.flatten() == "·"):
        problem.draw_board()
        if problem.player_turn == "x":
            move = iterative_deepening(
                problem, strategy, 5, 10
            )  # Adjust depth and timeout as needed
            if move:
                problem.place_move(*move, "x")
                print("AI placed at:", move)
        else:
            move = tuple(map(int, input("Enter your move (row col): ").split()))
            while not problem.place_move(*move, "o"):
                print("Invalid move, try again.")
                move = tuple(map(int, input("Enter your move (row col): ").split()))
        problem.player_turn = "o" if problem.player_turn == "x" else "x"
        os.system("cls" if os.name == "nt" else "clear")

    problem.draw_board()
    if problem.check_winner("x"):
        print("AI wins!")
    elif problem.check_winner("o"):
        print("Player wins!")
    else:
        print("It's a draw!")


play_game()
