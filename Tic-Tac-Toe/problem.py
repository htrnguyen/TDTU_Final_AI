import numpy as np
class Problem:
    def __init__(self, ai_player="o", human_player="x"):
        self.size = 8
        self.board = np.full((self.size, self.size), "·")
        self.ai_player = ai_player
        self.human_player = human_player
        self.current_player = self.human_player
        self.transposition_table = {}

    # Draw the board 8x8 in the console
    def draw_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(str(i) + " " + " ".join(self.board[i]))

    # Check if the move is valid
    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "·"

    # Make a move on the board
    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    # Undo a move on the board
    def undo_move(self, x, y):
        self.board[x][y] = "·"

    # Hash the board, ex: 123456789
    def hash_board(self):
        return hash(self.board.tobytes())

    # Get all the lines on the board (rows, columns, diagonals)
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

    # Check if a player has won
    def check_winner(self, player):
        lines = self.get_all_lines()
        win_condition = np.array([player] * 4)

        for line in lines:
            if len(line) >= 4:
                for i in range(len(line) - 3):
                    if np.array_equal(line[i : i + 4], win_condition):
                        return True
        return False

    # Check if the game is over
    def is_goal(self):
        return any(self.check_winner(p) for p in ["x", "o"]) or not np.any(
            self.board == "·"
        )

    # Get all possible moves
    def get_possible_moves(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == "·"
        ]

    # Evaluate the board
    def evaluate(self):
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            score += self.evaluate_line(line, self.ai_player) - self.evaluate_line(
                line, self.human_player
            )
        return score

    # Evaluate a line (row, column, diagonal)
    def evaluate_line(self, line, player):
        opponent = "o" if player == "x" else "x"
        line_score = 0
        line_str = "".join(line)

        # Patterns to evaluate (4 in a row, 3 in a row, 2 in a row, 1 in a row, empty spaces)
        patterns = {
            f"{player}{player}{player}{player}": 1000,
            f"{player}{player}{player}·": 100,
            f"{player}{player}·{player}": 100,
            f"{player}·{player}{player}": 100,
            f"·{player}{player}{player}": 100,
            f"{player}{player}··": 10,
            f"{player}·{player}·": 10,
            f"·{player}{player}·": 10,
            f"··{player}{player}": 10,
            f"{player}··{player}": 10,
            f"{player}·{player}": 1,
            f"·{player}{player}": 1,
            f"{player}··": 1,
            f"··{player}": 1,
            f"{player}": 0.1,
            f"{opponent}{opponent}{opponent}{opponent}": -1000,
            f"{opponent}{opponent}{opponent}·": -100,
            f"{opponent}{opponent}·": -100,
            f"{opponent}·{opponent}{opponent}": -100,
            f"·{opponent}{opponent}{opponent}": -100,
            f"{opponent}{opponent}··": -10,
            f"{opponent}·{opponent}·": -10,
            f"·{opponent}{opponent}·": -10,
            f"··{opponent}{opponent}": -10,
            f"{opponent}··{opponent}": -10,
            f"{opponent}·{opponent}": -1,
            f"·{opponent}{opponent}": -1,
            f"{opponent}··": -1,
            f"··{opponent}": -1,
            f"{opponent}": -0.1,
        }

        for pattern, value in patterns.items():
            line_score += line_str.count(pattern) * value

        return line_score