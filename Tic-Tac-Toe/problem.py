import os
from collections import defaultdict

import numpy as np


class Problem:
    def __init__(self):
        self.size = 8
        self.board = np.full((self.size, self.size), "·")
        self.player_turn = "x"
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
        for x in range(self.size):
            for y in range(self.size):
                if y <= self.size - 4 and np.all(self.board[x, y : y + 4] == player):
                    return True
                if x <= self.size - 4 and np.all(self.board[x : x + 4, y] == player):
                    return True
                if (
                    x <= self.size - 4
                    and y <= self.size - 4
                    and np.all([self.board[x + i, y + i] == player for i in range(4)])
                ):
                    return True
                if (
                    x >= 3
                    and y <= self.size - 4
                    and np.all([self.board[x - i, y + i] == player for i in range(4)])
                ):
                    return True
        return False

    def get_possible_moves(self):
        return [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.board[x, y] == "·"
        ]

    def utility(self, player):
        opponent = "x" if player == "o" else "o"
        score = 0
        center_bonus = 1.5  # More weight for center pieces
        # Additional weight for threat detection
        threat_multiplier = 10

        for x in range(self.size):
            for y in range(self.size):
                # Check all potential lines from this point
                if y <= self.size - 4:  # Horizontal
                    line = self.board[x, y : y + 4]
                    score += self.evaluate_line(line, player)
                    # Detect and react to immediate threats
                    if (
                        np.count_nonzero(line == opponent) == 3
                        and np.count_nonzero(line == "·") == 1
                    ):
                        score -= threat_multiplier * self.evaluate_line(line, opponent)

                if x <= self.size - 4:  # Vertical
                    line = self.board[x : x + 4, y]
                    score += self.evaluate_line(line, player)
                    if (
                        np.count_nonzero(line == opponent) == 3
                        and np.count_nonzero(line == "·") == 1
                    ):
                        score -= threat_multiplier * self.evaluate_line(line, opponent)

                if x <= self.size - 4 and y <= self.size - 4:  # Main diagonal
                    line = self.board[
                        np.ix_([x + i for i in range(4)], [y + i for i in range(4)])
                    ].diagonal()
                    score += self.evaluate_line(line, player)
                    if (
                        np.count_nonzero(line == opponent) == 3
                        and np.count_nonzero(line == "·") == 1
                    ):
                        score -= threat_multiplier * self.evaluate_line(line, opponent)

                if x >= 3 and y <= self.size - 4:  # Anti-diagonal
                    line = self.board[
                        np.ix_([x - i for i in range(4)], [y + i for i in range(4)])
                    ].diagonal()
                    score += self.evaluate_line(line, player)
                    if (
                        np.count_nonzero(line == opponent) == 3
                        and np.count_nonzero(line == "·") == 1
                    ):
                        score -= threat_multiplier * self.evaluate_line(line, opponent)

                # Center bonus
                if x == self.size // 2 and y == self.size // 2:
                    score += center_bonus * self.evaluate_line(
                        np.array([self.board[x, y]]), player
                    )
        return score

    def evaluate_line(self, line, player):
        opponent = "x" if player == "o" else "o"
        score = 0
        player_count = np.count_nonzero(line == player)
        opponent_count = np.count_nonzero(line == opponent)
        empty_count = np.count_nonzero(line == "·")

        if player_count == 4:
            score += 10000  # Win
        elif opponent_count == 4:
            score -= 10000  # Block win
        elif player_count == 3 and empty_count == 1:
            score += 5000  # Almost winning
        elif opponent_count == 3 and empty_count == 1:
            score -= 5000  # Block opponent almost winning
        elif player_count == 2 and empty_count == 2:
            score += 2000  # Developing opportunity
        elif opponent_count == 2 and empty_count == 2:
            score -= 2000  # Block developing opportunity of opponent
        elif player_count == 1 and empty_count == 3:
            score += 1000  # Potential opportunity
        elif opponent_count == 1 and empty_count == 3:
            score -= 1000  # Potential threat
        elif player_count == 3 and opponent_count == 1:
            score += 500  # Potential opportunity
        elif opponent_count == 3 and player_count == 1:
            score -= 500  # Potential threat
        elif player_count == 2 and opponent_count == 2:
            score += 100  # Stalemate
        elif opponent_count == 2 and player_count == 2:
            score -= 100  # Stalemate

        return score


class SearchStrategy:
    transposition_table = defaultdict(lambda: (None, None))

    def get_sorted_moves(self, problem, player):
        moves = problem.get_possible_moves()
        moves.sort(
            key=lambda move: self.simulate_move(problem, move, player), reverse=True
        )
        return moves

    def simulate_move(self, problem, move, player):
        x, y = move
        problem.place_move(x, y, player)
        score = problem.utility(player)
        problem.undo_move(x, y)
        return score

    def alpha_beta_search(self, problem, depth, alpha, beta, maximizingPlayer):
        state_key = hash(problem.board.tostring())
        
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0 or problem.is_goal():
            score = problem.utility("o" if maximizingPlayer else "x")
            self.transposition_table[state_key] = (None, score)
            return None, score

        best_move = None
        if maximizingPlayer:
            max_eval = float("-inf")
            for x, y in self.get_sorted_moves(problem, "o"):
                problem.place_move(x, y, "o")
                _, eval = self.alpha_beta_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(x, y)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = (best_move, max_eval)
            return best_move, max_eval
        else:
            min_eval = float("inf")
            for x, y in self.get_sorted_moves(problem, "x"):
                problem.place_move(x, y, "x")
                _, eval = self.alpha_beta_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(x, y)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[state_key] = (best_move, min_eval)
            return best_move, min_eval


def iterative_deepening_search(problem, strategy, max_depth=10):
    best_move = None
    best_eval = float("-inf")
    for depth in range(1, max_depth + 1):
        move, eval = strategy.alpha_beta_search(
            problem, depth, float("-inf"), float("inf"), True
        )
        if eval > best_eval:
            best_move = move
            best_eval = eval
    return best_move


# Main
def test():
    problem = Problem()
    search_strategy = SearchStrategy()
    problem.draw_board()
    player = problem.player_turn

    while True:
        if player == "x":
            x, y = map(int, input("Enter move (x y): ").split())
            while not problem.place_move(x, y, player):
                print("Invalid move. Please enter again.")
                x, y = map(int, input("Enter move (x y): ").split())

        else:
            print("AI's turn")
            move = iterative_deepening_search(problem, search_strategy, max_depth=30)
            if move:
                x, y = move
                problem.place_move(x, y, player)
                print(f"AI placed at {x} {y}")

        # Clear the console and redraw the board
        os.system("cls" if os.name == "nt" else "clear")
        problem.draw_board()

        # Check if there is a winner or the game is a draw
        if problem.check_winner(player):
            print(f"{player} wins!")
            break
        elif np.all(problem.board != "·"):
            print("It's a draw!")
            break

        # Switch player
        player = "o" if player == "x" else "x"

    print("Game over!")


test()
