import time

import numpy as np


class TicTacToe:
    def __init__(self):
        self.size = 8
        self.board = np.full((self.size, self.size), "-")
        self.player_turn = "x"
        self.transposition_table = {}

    def draw_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(str(i) + " " + " ".join(self.board[i]))

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "-"

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        self.board[x][y] = "-"

    def check_winner(self, player):
        lines = []
        for i in range(self.size):
            lines.append(self.board[i, :])
            lines.append(self.board[:, i])

        diagonals = [self.board.diagonal(i) for i in range(-self.size + 1, self.size)]
        diagonals.extend(
            self.board[:, ::-1].diagonal(i) for i in range(-self.size + 1, self.size)
        )
        lines.extend(diagonals)

        win_condition = np.array([player] * 4)
        for line in lines:
            if len(line) >= 4:
                for i in range(len(line) - 3):
                    if np.array_equal(line[i : i + 4], win_condition):
                        return True
        return False

    def is_terminal(self):
        return any(self.check_winner(p) for p in ["x", "o"]) or not np.any(
            self.board == "-"
        )

    def get_possible_moves(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == "-"
        ]

    def hash_board(self):
        return hash(self.board.tostring())

    def evaluate(self):
        score = 0
        lines = []
        for i in range(self.size):
            lines.append(self.board[i, :])
            lines.append(self.board[:, i])
        diagonals = [self.board.diagonal(i) for i in range(-self.size + 1, self.size)]
        diagonals.extend(
            self.board[:, ::-1].diagonal(i) for i in range(-self.size + 1, self.size)
        )
        lines.extend(diagonals)

        # Evaluate each line for both players
        for line in lines:
            score += self.evaluate_line(line, "x") - self.evaluate_line(line, "o")
        return score

    def evaluate_line(self, line, player):
        opponent = "o" if player == "x" else "x"
        line_score = 0
        line_str = "".join(line)
        patterns = {
            f"{player}{player}{player}{player}": 100000,  # Immediate win
            f"{player}{player}{player}-": 1000,  # Threat to win
            f"-{player}{player}{player}": 1000,  # Threat to win
            f"{player}{player}-": 100,  # Two with space
            f"-{player}{player}": 100,  # Two with space
            f"{player}-": 10,  # Single piece potential
            f"-{player}": 10,  # Single piece potential
            f"{player}{player}- -{player}": 1500,  # Split three (flexible threat)
            f"{player}- -{player}{player}": 1500,  # Split three (flexible threat)
        }

        # Add score for player patterns
        for pattern, value in patterns.items():
            occurrences = line_str.count(pattern)
            line_score += occurrences * value

        # Check for opponent's threats and increase their score impact
        threat_patterns = {
            f"{opponent}{opponent}{opponent}{opponent}": -100000,  # Opponent wins
            f"{opponent}{opponent}{opponent}-": -1000,  # Block opponent's next move win
            f"-{opponent}{opponent}{opponent}": -1000,  # Block opponent's next move win
            f"{opponent}{opponent}- -{opponent}": -1500,  # Block flexible threat
            f"{opponent}- -{opponent}{opponent}": -1500,  # Block flexible threat
        }

        # Add score for blocking opponent patterns
        for pattern, value in threat_patterns.items():
            occurrences = line_str.count(pattern)
            line_score += occurrences * value

        return line_score


class SearchStrategy:
    def alpha_beat_search(
        self,
        problem,
        depth,
        alpha,
        beta,
        max_player=True,
    ):
        board_hash = problem.hash_board()
        if board_hash in problem.transposition_table:
            return problem.transposition_table[board_hash], None

        if depth == 0 or problem.is_terminal():
            return problem.evaluate(), None

        best_move = None
        if max_player:
            max_value = float("-inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, "x")
                eval, _ = self.alpha_beat_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(*move)

                if eval > max_value:
                    max_value = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[board_hash] = max_value
            return max_value, best_move
        else:
            min_value = float("inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, "o")
                eval, _ = self.alpha_beat_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)

                if eval < min_value:
                    min_value = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[board_hash] = min_value
            return min_value, best_move

    def find_best_move(self, problem, depth=4):
        best_move = None
        best_value = float("-inf")

        for depth in range(1, depth + 1):
            value, move = self.alpha_beat_search(
                problem, depth, float("-inf"), float("inf"), True
            )
            if value > best_value:
                best_value = value
                best_move = move

            print(f"Depth: {depth} - Best value: {best_value} - Move: {best_move}")
        print(f"Best value: {best_value} - Move: {best_move} - Depth: {depth}")
        return best_move


# Play the game
def play_game():
    game = TicTacToe()
    search = SearchStrategy()

    while True:
        game.draw_board()

        if game.player_turn == "x":
            x, y = map(int, input("Enter your move: ").split())
            while not game.is_valid_move(x, y):
                x, y = map(int, input("Invalid move. Enter your move: ").split())
            game.make_move(x, y, "x")
        else:
            print("AI is thinking...")
            x, y = search.find_best_move(game)
            game.make_move(x, y, "o")
        game.player_turn = "o" if game.player_turn == "x" else "x"

        if game.check_winner("x"):
            game.draw_board()
            print("You win!")
            break
        if game.check_winner("o"):
            game.draw_board()
            print("AI wins!")
            break
        if game.is_terminal():
            game.draw_board()
            print("It's a draw!")
            break


play_game()
