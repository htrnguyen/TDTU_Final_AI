import time

import numpy as np


class TicTacToe:
    def __init__(self):
        self.size = 8
        self.board = np.full((self.size, self.size), "-")
        self.ai_player = "o"
        self.human_player = "x"
        self.current_player = self.human_player
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
        lines = self.get_all_lines()
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
        return hash(self.board.tobytes())

    def get_all_lines(self):
        lines = []
        for i in range(self.size):
            lines.append(self.board[i, :])
            lines.append(self.board[:, i])
        diagonals = [self.board.diagonal(i) for i in range(-self.size + 1, self.size)]
        diagonals.extend(
            self.board[:, ::-1].diagonal(i) for i in range(-self.size + 1, self.size)
        )
        lines.extend(diagonals)
        return lines

    def evaluate(self):
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            score += self.evaluate_line(line, self.ai_player) - self.evaluate_line(
                line, self.human_player
            )
        return score

    def evaluate_line(self, line, player):
        opponent = "o" if player == "x" else "x"
        line_score = 0
        line_str = "".join(line)

        patterns = {
            f"{player}{player}{player}{player}": 1000,
            f"{player}{player}{player}-": 100,
            f"{player}{player}-{player}": 100,
            f"{player}-{player}{player}": 100,
            f"-{player}{player}{player}": 100,
            f"{player}{player}--": 10,
            f"{player}-{player}-": 10,
            f"-{player}{player}-": 10,
            f"--{player}{player}": 10,
            f"{player}--{player}": 10,
            f"{player}-{player}": 1,
            f"-{player}{player}": 1,
            f"{player}--": 1,
            f"--{player}": 1,
            f"{player}": 0.1,
            f"{opponent}{opponent}{opponent}{opponent}": -1000,
            f"{opponent}{opponent}{opponent}-": -100,
            f"{opponent}{opponent}-": -100,
            f"{opponent}-{opponent}{opponent}": -100,
            f"-{opponent}{opponent}{opponent}": -100,
            f"{opponent}{opponent}--": -10,
            f"{opponent}-{opponent}-": -10,
            f"-{opponent}{opponent}-": -10,
            f"--{opponent}{opponent}": -10,
            f"{opponent}--{opponent}": -10,
            f"{opponent}-{opponent}": -1,
            f"-{opponent}{opponent}": -1,
            f"{opponent}--": -1,
            f"--{opponent}": -1,
            f"{opponent}": -0.1,
        }

        for pattern, value in patterns.items():
            line_score += line_str.count(pattern) * value

        return line_score


class SearchStrategy:
    def alpha_beta_search(self, problem, depth, alpha, beta, maximizing_player):
        hash_board = problem.hash_board()
        if hash_board in problem.transposition_table:
            return problem.transposition_table[hash_board], None

        if depth == 0 or problem.is_terminal():
            return problem.evaluate(), None

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, problem.ai_player)
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(*move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[hash_board] = max_eval
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, problem.human_player)
                eval, _ = self.alpha_beta_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[hash_board] = min_eval
            return min_eval, best_move

    def find_best_move(self, problem, depth=3):
        best_move = None
        best_value = float("-inf")

        for depth in range(1, depth + 1):
            value, move = self.alpha_beta_search(
                problem, depth, float("-inf"), float("inf"), True
            )

            if value > best_value:
                best_value = value
                best_move = move

        print(f"Best value: {best_value}, Move: {best_move}, Depth: {depth}")

        return best_move


# Play the game
def play_game():
    game = TicTacToe()
    search = SearchStrategy()
    while not game.is_terminal():
        game.draw_board()
        if game.current_player == game.human_player:
            x, y = map(int, input("Enter your move (x y): ").split())
            while not game.make_move(x, y, game.human_player):
                print("Invalid move. Try again.")
                x, y = map(int, input("Enter your move (x y): ").split())
        else:
            print("AI is thinking...")
            move = search.find_best_move(game, depth=4)
            if move:
                game.make_move(*move, game.ai_player)
                print(f"AI plays at {move[0]}, {move[1]}")
        game.current_player = (
            game.ai_player
            if game.current_player == game.human_player
            else game.human_player
        )
        if game.check_winner(game.human_player):
            game.draw_board()
            print("You win!")
            break
        elif game.check_winner(game.ai_player):
            game.draw_board()
            print("AI wins!")
            break
        if game.is_terminal():
            game.draw_board()
            print("It's a draw!")
            break


play_game()
