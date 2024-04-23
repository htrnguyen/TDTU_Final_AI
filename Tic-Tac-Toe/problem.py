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

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "·"

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        self.board[x][y] = "·"

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

    def check_winner(self, player):
        lines = self.get_all_lines()
        win_condition = np.array([player] * 4)

        for line in lines:
            if len(line) >= 4:
                for i in range(len(line) - 3):
                    if np.array_equal(line[i : i + 4], win_condition):
                        return True
        return False
    
    def is_goal(self):
        return any(self.check_winner(p) for p in ["x", "o"]) or not np.any(
            self.board == "·"
        )

    def get_possible_moves(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == "·"
        ]

    def evaluate_line(self, line, player):
        opp_player = "o" if player == "x" else "x"
        line_score = 0

        for i in range(len(line) - 3):
            segment = line[i : i + 4]
            count_player = np.count_nonzero(segment == player)
            count_opp = np.count_nonzero(segment == opp_player)
            count_open = np.count_nonzero(segment == "·")

            # Đánh giá cho AI
            if count_player == 4:
                line_score += 10000  # Chiến thắng
            elif count_player == 3 and count_open == 1:
                line_score += 500  # Sắp thắng
            elif count_player == 2 and count_open == 2:
                line_score += 100  # Phát triển dãy thắng
            elif count_player == 1 and count_open == 3:
                line_score += 10  # Phát triển dãy thắng

            # Phát hiện và đánh giá các mối đe dọa từ đối thủ
            if count_opp == 3 and count_open == 1:
                line_score -= 800  # Đối thủ sắp thắng, cần chặn
            if count_opp == 2 and count_open == 2:
                line_score -= 400  # Đối thủ có khả năng phát triển thành dãy thắng
            if count_opp == 1 and count_open == 3:
                line_score -= 40
        return line_score

    def evaluate(self):
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            score += self.evaluate_line(line, "x")
            score -= self.evaluate_line(line, "o")

        return score
