import numpy as np
import regex as re
from board import Board

class Problem:
    UTILITY = {
        "Quintet": [20000000, ["xxxx"]],
        "Quartet_2Opens": [400000, ["exxxe"]],
        "Quartet_1Open": [50000, ["bxxxxe", "exxxxb"]],
        "Triplet_2Opens": [30000, ["exxxe"]],
        "Triplet_1Open": [15000, ["bxxxe", "exxxb"]],
        "ProbQuartet_2Opens": [7000, ["exexxe", "exxexe"]],
        "ProbQuartet_1Open": [3000, ["bxexxe", "bxxexe", "exxexb", "exexxb"]],
        "Double_2Opens": [500, ["exxee", "eexxe"]],
        "Double_1Open": [400, ["bxxee", "eexxb"]],
        "Double_1Open_1Blocked": [200, ["bxxe"]],
        "nProbTriplet_2Opens": [100, ["exexe"]],
        "ProbTriplet_1Open": [40, ["bxexee", "eexexb"]],
    }

    def __init__(self, board, human_player="X"):
        self.board = board
        self.human_player = human_player
        self.ai_player = "O" if human_player == "X" else "X"
        self.current_player = self.human_player

    def switch_player(self):
        self.current_player = (
            self.ai_player
            if self.current_player == self.human_player
            else self.human_player
        )

    def check_winner(self, player):
        lines = self.board.get_all_lines()
        return np.any(["".join(line).find(player * 4) != -1 for line in lines])

    def is_goal(self):
        return (
            self.check_winner(self.human_player)
            or self.check_winner(self.ai_player)
            or self.board.is_full()
        )

    def evaluate(self):
        return self.calculate_heuristic(self.board.board, self.ai_player)

    def search_in_list(self, lists, search_for):
        search_for_compiled = re.compile(search_for)
        return sum(
            len(search_for_compiled.findall(lst, overlapped=True)) for lst in lists
        )

    def make_lines(self, matrix, player):
        lines = []
        trans = {player: "x", "-": "e"}

        def translate(arr):
            return "".join([trans.get(c, "b") for c in arr])

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
            return np.sum(player_board * Board.HEURISTIC)

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
        temp_board = self.board.board.copy()
        temp_board[x][y] = self.ai_player
        score = self.calculate_heuristic(temp_board, self.ai_player)
        return score

    def get_valid_moves(self):
        return list(zip(*np.where(self.board.board == "-")))

    def sort_moves(self):
        center = self.board.size // 2
        valid_moves = self.get_valid_moves()
        return sorted(
            valid_moves,
            key=lambda move: (abs(move[0] - center) + abs(move[1] - center)),
        )
