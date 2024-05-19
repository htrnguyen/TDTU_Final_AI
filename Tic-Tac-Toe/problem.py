import heapq

import numpy as np
import regex as re
from board import Board


class Problem:
    """
    Quản lý trạng thái của game và các hàm liên quan
    """

    def __init__(self, size=8, human_player="X", opponent_factor=1.05):
        """
        Khởi tạo trạng thái game
        """
        self.board = Board(size)
        self.human_player = human_player
        self.ai_player = "O" if human_player == "X" else "X"
        self.opponent_factor = opponent_factor
        self.current_player = self.human_player
        self.HEURISTIC = self.generate_heuristic(size)
        self.evaluation_cache = {}

    def generate_heuristic(self, size):
        """
        Tạo mảng 2 chiều lưu giá trị heuristic cho mỗi ô
        Giá trị heuristic = min(i, j, size - i - 1, size - j - 1)
        Example: size = 3
            0 0 0
            0 1 0
            0 0 0
        """
        heuristic = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                heuristic[i][j] = min(i, j, size - i - 1, size - j - 1)
        return heuristic

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
        board_hash = self.hash_board()
        if board_hash in self.evaluation_cache:
            return self.evaluation_cache[board_hash]

        score = self.calculate_heuristic(self.board.board, self.ai_player)
        self.evaluation_cache[board_hash] = score
        return score

    def hash_board(self):
        """
        Hash bàn cờ
        """
        return hash(self.board.board.tostring())

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

        """
        UTILITY: giá trị đánh giá cho các trường hợp trên bàn cờ
        """
        UTILITY = {
            "FourInRow": [1000000, ["xxxx"]],
            "KillerMove": [100000, ["exxx", "xxxe"]],
            "ThreeInRow_OpenBothEnds": [50000, ["exxxe"]],
            "ThreeInRow_OneOpenEnd": [10000, ["bxxxe", "exxxb"]],
            "TwoInRow_OpenBothEnds": [5000, ["exxe", "eexx", "xxee"]],
            "TwoInRow_OneOpenEnd": [1000, ["bxxe", "eexb", "exxb", "bexx"]],
            "PotentialThreeInRow_OpenBothEnds": [700, ["exexxe", "exxexe", "eexexx"]],
            "PotentialThreeInRow_OneOpenEnd": [
                300,
                ["bxexxe", "bxxexe", "exxexb", "exexxb", "eexexb", "eexbxx"],
            ],
            "SinglePiece_OpenBothEnds": [50, ["exee", "eeex"]],
            "SinglePiece_OneOpenEnd": [40, ["bxe", "eexb"]],
            "SinglePiece_OneOpenOneBlocked": [20, ["bxe"]],
            "PotentialTwoInRow_OpenBothEnds": [10, ["exxe"]],
            "PotentialSinglePiece_OneOpenEnd": [4, ["bxeee", "eeexb"]],
        }

        def get_sequence_score(lines):
            """
            Tính giá trị heuristic dựa trên các pattern
            """
            sequence_score = 0
            for _, (value, patterns) in UTILITY.items():
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
            return np.sum(player_board * self.HEURISTIC)

        lines = self.generate_lines(board, player)
        player_score = get_sequence_score(lines) + get_position_score(board, player)

        opponent = "O" if player == "X" else "X"
        opponent_lines = self.generate_lines(board, opponent)
        opponent_score = get_sequence_score(opponent_lines) + get_position_score(
            board, opponent
        )

        return player_score - self.opponent_factor * opponent_score

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
        Sắp xếp các nước đi tiềm năng dựa trên giá trị heuristic
        """
        moves = []
        heuristic = self.HEURISTIC

        empty_positions = np.argwhere(self.board.board == self.board.empty)
        for x, y in empty_positions:
            move_score = heuristic[x][y]
            heapq.heappush(moves, (-move_score, x, y))

        sorted_moves = [heapq.heappop(moves) for _ in range(len(moves))]
        return [(x, y) for _, x, y in sorted_moves]
