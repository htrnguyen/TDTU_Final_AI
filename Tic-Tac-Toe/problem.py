import os
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
        self.pattern_scores = {
            "xxxx": 10000,
            "ooo": -5000,
            "xx·x": 500,
            "x·xx": 500,
            "·xxx·": 2000,
            "·xx·": 100,
            "·oo·": -100,
            "x·x": 50,
            "o·o": -50,
        }

    def evaluate_board(self, board):
        score = 0
        lines = []
        for d in range(-board.shape[0] + 1, board.shape[0]):
            lines.append(
                "".join(
                    [
                        board[i, i + d]
                        for i in range(board.shape[0])
                        if 0 <= i < board.shape[0] and 0 <= i + d < board.shape[0]
                    ]
                )
            )
            lines.append(
                "".join(
                    [
                        board[i + d, i]
                        for i in range(board.shape[0])
                        if 0 <= i < board.shape[0] and 0 <= i + d < board.shape[0]
                    ]
                )
            )

        for x in range(board.shape[0]):
            lines.append("".join(board[x, :]))
            lines.append("".join(board[:, x]))

        for line in lines:
            for pattern, value in self.pattern_scores.items():
                if pattern in line:
                    score += value
        return score

    def alpha_beta_search(self, problem, depth, alpha, beta, maximizing_player):
        if depth == 0 or problem.is_goal():
            return self.evaluate_board(problem.board), None

        best_move = None
        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            moves = sorted(
                problem.get_possible_moves(),
                key=lambda m: self.evaluate_board_after_move(
                    problem.board, m, problem.player_turn
                ),
                reverse=True,
            )
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
            return max_eval, best_move
        else:
            min_eval = float("inf")
            moves = sorted(
                problem.get_possible_moves(),
                key=lambda m: self.evaluate_board_after_move(
                    problem.board, m, problem.player_turn
                ),
            )
            for move in moves:
                problem.place_move(*move, problem.player_turn)
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board_after_move(self, board, move, player):
        x, y = move
        board[x, y] = player
        score = self.evaluate_board(board)
        board[x, y] = "·"
        return score


# Main
def play_game():
    problem = Problem()
    search_strategy = SearchStrategy()
    max_depth = 4  # Adjust depth based on game state if necessary
    while not problem.is_goal() and any(problem.board.flatten() == "·"):
        problem.draw_board()
        if problem.player_turn == "x":
            print("AI's turn")
            _, move = search_strategy.alpha_beta_search(
                problem, max_depth, float("-inf"), float("inf"), True
            )
            if move:
                problem.place_move(*move, "x")
                print("AI placed at:", move)
        else:
            move = tuple(map(int, input("Enter your move (row col): ").split()))
            while not problem.place_move(*move, "o"):
                print("Invalid move, try again.")
                move = tuple(map(int, input("Enter your move (row col): ").split()))
        problem.player_turn = "o" if problem.player_turn == "x" else "x"
        # os.system("cls" if os.name == "nt" else "clear")

    problem.draw_board()
    if problem.check_winner("x"):
        print("AI wins!")
    elif problem.check_winner("o"):
        print("Player wins!")
    else:
        print("It's a draw!")


play_game()