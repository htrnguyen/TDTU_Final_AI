import numpy as np
import regex as re
from collections import Counter


class Problem:
    UTILITY = {
        "Quintet": [20000000, ["xxxx"]],
        "Quartet_2Opens": [400000, ["exxxe"]],
        "Quartet_1Open": [50000, ["nxxxxe", "exxxxn"]],
        "Triplet_2Opens": [30000, ["exxxe"]],
        "Triplet_1Open": [15000, ["nxxxe", "exxxn"]],
        "ProbQuartet_2Opens": [7000, ["exexxe", "exxexe"]],
        "ProbQuartet_1Open": [3000, ["nxexxe", "nxxexe", "exxexn", "exexxn"]],
        "Double_2Opens": [500, ["exxee", "eexxe"]],
        "Double_1Open": [400, ["nxxee", "eexxn"]],
        "nProbTriplet_2Opens": [100, ["exexe"]],
        "ProbTriplet_1Open": [40, ["nxexee", "eexexn"]],
    }

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

    def __init__(self, size=8, human_player="X"):
        self.size = size
        self.board = np.full((self.size, self.size), "-")
        self.human_player = human_player
        self.ai_player = "O" if human_player == "X" else "X"
        self.current_player = self.human_player

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

    def switch_player(self):
        self.current_player = (
            self.ai_player
            if self.current_player == self.human_player
            else self.human_player
        )

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

    def check_winner(self, player):
        lines = self.get_all_lines()
        return np.any(["".join(line).find(player * 4) != -1 for line in lines])

    def is_full(self):
        return not np.any(self.board == "-")

    def is_goal(self):
        return (
            self.check_winner(self.human_player)
            or self.check_winner(self.ai_player)
            or self.is_full()
        )

    def evaluate(self):
        return self.calculate_heuristic(self.board, self.ai_player)

    def search_in_list(self, lists, search_for):
        search_for_compiled = re.compile(search_for)
        return sum(
            len(search_for_compiled.findall(lst, overlapped=True)) for lst in lists
        )

    def make_lines(self, matrix, player):
        lines = []
        trans = {player: "x", "-": "e"}

        def translate(arr):
            return "".join([trans.get(c, "n") for c in arr])

        lines = [translate(row) for row in matrix]
        lines += [translate(col) for col in matrix.T]

        for i in range(-matrix.shape[0] + 1, matrix.shape[1]):
            lines += [
                translate(np.diagonal(matrix, i)),
                translate(np.diagonal(np.fliplr(matrix), i)),
            ]

        return lines

    def calculate_heuristic(self, board, player):
        def get_sequence_heuristic(lines):
            sequence_heuristic = 0
            for key, (value, patterns) in self.UTILITY.items():
                for pattern in patterns:
                    sequence_heuristic += value * self.search_in_list(lines, pattern)
            return sequence_heuristic

        def get_position_heuristic(board, player):
            player_board = np.where(board == player, 1, 0)
            return np.sum(player_board * self.HEURISTIC)

        lines = self.make_lines(board, player)
        player_score = get_sequence_heuristic(lines) + get_position_heuristic(
            board, player
        )

        opponent = "O" if player == "X" else "X"
        lines_opponent = self.make_lines(board, opponent)
        opponent_score = get_sequence_heuristic(
            lines_opponent
        ) + get_position_heuristic(board, opponent)

        return player_score - 1.05 * opponent_score

    def evaluate_move(self, move):
        x, y = move
        temp_board = self.board.copy()
        temp_board[x][y] = self.ai_player
        score = self.calculate_heuristic(temp_board, self.ai_player)
        return score

    def sort_moves(self):
        valid_moves = self.get_valid_moves()
        scores = {move: self.evaluate_move(move) for move in valid_moves}
        return sorted(valid_moves, key=lambda move: -scores[move])

    def get_valid_moves(self):
        return list(zip(*np.where(self.board == "-")))


class SearchStrategy:
    def alpha_beta_search(self, problem, max_depth=2):

        def max_value(problem, alpha, beta, depth):
            if problem.is_goal() or depth >= max_depth:
                return problem.evaluate()

            value = float("-inf")
            for move in problem.get_valid_moves():
                problem.make_move(move[0], move[1], problem.ai_player)
                value = max(value, min_value(problem, alpha, beta, depth + 1))
                problem.undo_move(move[0], move[1])
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        def min_value(problem, alpha, beta, depth):
            if problem.is_goal() or depth >= max_depth:
                return problem.evaluate()

            value = float("inf")
            for move in problem.get_valid_moves():
                problem.make_move(move[0], move[1], problem.human_player)
                value = min(value, max_value(problem, alpha, beta, depth + 1))
                problem.undo_move(move[0], move[1])
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        alpha = float("-inf")
        beta = float("inf")
        best_value = float("-inf")
        best_move = None

        for move in sorted(
            problem.get_valid_moves(),
            key=lambda x: problem.evaluate_move(x),
            reverse=True,
        ):
            problem.make_move(move[0], move[1], problem.ai_player)
            value = min_value(problem, alpha, beta, 1)
            problem.undo_move(move[0], move[1])
            if value > best_value:
                best_value = value
                best_move = move
                print(f"Best move: {best_move}, value: {best_value}")
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        return best_move


def play_game():
    problem = Problem()
    strategy = SearchStrategy()

    while not problem.is_goal():
        problem.draw_board()
        if problem.current_player == problem.human_player:
            x, y = map(int, input("Enter your move: ").split())
            if problem.make_move(x, y, problem.human_player):
                problem.switch_player()
            else:
                print("Invalid move")
        else:
            move = strategy.alpha_beta_search(problem)
            problem.make_move(move[0], move[1], problem.ai_player)
            problem.switch_player()

    problem.draw_board()
    if problem.check_winner(problem.human_player):
        print("You win!")
    elif problem.check_winner(problem.ai_player):
        print("You lose!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play_game()
