import numpy as np
import regex as re
from board import Board


class Problem:
    """
    Quản lý trạng thái của game và các hàm liên quan
    """

    """
    UTILITY: giá trị đánh giá cho các trường hợp trên bàn cờ
    """
    UTILITY = {
        "Quartet": [20000000, ["xxxx"]],
        "Triplet_2Opens": [400000, ["exxxe"]],
        "Triplet_1Open": [50000, ["bxxxe", "exxxb"]],
        "Double_2Opens": [30000, ["exxe", "eexx"]],
        "Double_1Open": [15000, ["bxxe", "eexb"]],
        "ProbTriplet_2Opens": [7000, ["exexxe", "exxexe"]],
        "ProbTriplet_1Open": [3000, ["bxexxe", "bxxexe", "exxexb", "exexxb"]],
        "Single_2Opens": [500, ["exee", "eeex"]],
        "Single_1Open": [400, ["bxe", "eexb"]],
        "Single_1Open_1Blocked": [200, ["bxe"]],
        "nProbDouble_2Opens": [100, ["exxe"]],
        "ProbSingle_1Open": [40, ["bxeee", "eeexb"]],
    }

    def __init__(self, board, human_player="X"):
        """
        Khởi tạo trạng thái game
        """
        self.board = board
        self.human_player = human_player
        self.ai_player = "O" if human_player == "X" else "X"
        self.current_player = self.human_player

    def switch_player(self):
        """
        Đổi lượt chơi
        """
        self.current_player = (
            self.ai_player
            if self.current_player == self.human_player
            else self.human_player
        )

    def check_winner(self, player):
        """
        Kiểm tra chiến thắng của player
        """
        lines = self.board.get_all_lines()
        return np.any(["".join(line).find(player * 4) != -1 for line in lines])

    def is_game_over(self):
        """
        Kiểm tra game kết thúc (Goal state)
        """
        return (
            self.check_winner(self.human_player)
            or self.check_winner(self.ai_player)
            or self.board.is_full()
        )

    def get_valid_moves(self):
        """
        Lấy tất cả các nước đi hợp lệ
        """
        return list(zip(*np.where(self.board.board == self.board.empty)))

    def evaluate(self):
        """
        Hàm đánh giá trạng thái game
        """
        return self.calculate_heuristic(self.board.board, self.ai_player)

    def count_patterns_in_lines(self, lines, pattern):
        """
        Đếm số lần xuất hiện của pattern trong lines
        """
        compiled_pattern = re.compile(pattern)
        return sum(
            len(compiled_pattern.findall(line, overlapped=True)) for line in lines
        )

    def generate_lines(self, matrix, player):
        """
        Tạo ra tất cả các dòng, cột, đường chéo trên bàn cờ
        """
        lines = []
        trans = {player: "x", self.board.empty: "e"}

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
        """
        Tính giá trị heuristic của trạng thái game
        """

        def get_sequence_score(lines):
            """
            Tính giá trị heuristic dựa trên các pattern
            """
            sequence_score = 0
            for _, (value, patterns) in self.UTILITY.items():
                for pattern in patterns:
                    sequence_score += value * self.count_patterns_in_lines(
                        lines, pattern
                    )
            return sequence_score

        def get_position_score(board, player):
            """
            Tính giá trị heuristic dựa trên vị trí của các quân cờ
            """
            player_board = np.where(board == player, 1, 0)
            return np.sum(player_board * self.board.HEURISTIC)

        lines = self.generate_lines(board, player)
        player_score = get_sequence_score(lines) + get_position_score(board, player)

        opponent = "O" if player == "X" else "X"
        opponent_lines = self.generate_lines(board, opponent)
        opponent_score = get_sequence_score(opponent_lines) + get_position_score(
            board, opponent
        )

        return player_score - 1.05 * opponent_score

    def evaluate_move(self, move):
        """
        Đánh giá nước đi
        """
        x, y = move
        temp_board = self.board.board.copy()
        temp_board[x][y] = self.ai_player
        score = self.calculate_heuristic(temp_board, self.ai_player)
        return score

    def sort_moves(self):
        """
        Sắp xếp các nước đi theo thứ tự gần tâm bàn cờ
        """
        center = self.board.size // 2
        valid_moves = self.get_valid_moves()
        return sorted(
            valid_moves,
            key=lambda move: (abs(move[0] - center) + abs(move[1] - center)),
        )
