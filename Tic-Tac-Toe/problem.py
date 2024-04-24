import numpy as np


class Problem:
    def __init__(self):
        self.size = 8
        self.board = np.full((self.size, self.size), "·")
        self.player_turn = "x"
        self.transposition_table = {}

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

    def hash_board(self):
        return hash(self.board.tostring())

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

    def evaluate(self):
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            score += self.evaluate_line(line, "x") - self.evaluate_line(line, "o")
        return score

    def evaluate_line(self, line, player):
        opponent = "o" if player == "x" else "x"
        line_score = 0
        line_str = "".join(line)
        patterns = {
            f"{player}{player}{player}{player}": 100000,  # Immediate win
            f"{player}{player}{player}·": 1000,  # Threat to win
            f"-{player}{player}{player}": 1000,  # Threat to win
            f"{player}{player}·": 100,  # Two with space
            f"-{player}{player}": 100,  # Two with space
            f"{player}·": 10,  # Single piece potential
            f"-{player}": 10,  # Single piece potential
            f"{player}{player}· ·{player}": 1500,  # Split three (flexible threat)
            f"{player}· ·{player}{player}": 1500,  # Split three (flexible threat)
        }

        # Add score for player patterns
        for pattern, value in patterns.items():
            occurrences = line_str.count(pattern)
            line_score += occurrences * value

        # Check for opponent's threats and increase their score impact
        threat_patterns = {
            f"{opponent}{opponent}{opponent}{opponent}": -100000,  # Opponent wins
            f"{opponent}{opponent}{opponent}·": -1000,  # Block opponent's next move win
            f"-{opponent}{opponent}{opponent}": -1000,  # Block opponent's next move win
            f"{opponent}{opponent}· ·{opponent}": -1500,  # Block flexible threat
            f"{opponent}· ·{opponent}{opponent}": -1500,  # Block flexible threat
        }

        # Add score for blocking opponent patterns
        for pattern, value in threat_patterns.items():
            occurrences = line_str.count(pattern)
            line_score += occurrences * value

        return line_score
