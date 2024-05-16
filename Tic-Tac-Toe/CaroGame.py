import copy

import numpy as np


class Problem:
    def __init__(self, size=8, human_player="X"):
        self.size = size
        self.board = np.full((self.size, self.size), "-")
        self.human_player = human_player
        self.ai_player = "O" if human_player == "X" else "X"
        self.current_player = self.human_player

    def draw_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(str(i) + " " + " ".join(self.board[i]))

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

    def hash_board(self):
        return hash(self.board.tostring())

    def switch_player(self):
        self.current_player = (
            self.ai_player
            if self.current_player == self.human_player
            else self.human_player
        )

    def get_all_lines(self):
        lines = []
        lines.extend(self.board.tolist())
        lines.extend(self.board.T.tolist())
        for d in range(-self.size + 1, self.size):
            lines.append(np.diag(self.board, k=d).tolist())
            lines.append(np.diag(np.fliplr(self.board), k=d).tolist())
        lines = [line for line in lines if len(line) >= 4]
        return lines

    def check_winner(self, player):
        lines = self.get_all_lines()
        for line in lines:
            if "".join(line).find(player * 4) != -1:
                return True
        return False

    def is_full(self):
        return not np.any(self.board == "-")

    def is_goal(self):
        return (
            self.check_winner(self.human_player)
            or self.check_winner(self.ai_player)
            or self.is_full()
        )

    def get_valid_moves(self):
        return [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if self.is_valid_move((x, y))
        ]

    def evaluate(self, player):
        def eval_pos(line):
            score = 0
            if "XXXX" in line:
                score += 10000000
            elif "XXX-" in line or "-XXX" in line or "XX-X" in line:
                score += 100000
            elif "XX-" in line or "-XX" in line or "X-X" in line:
                score += 100
            if "OOOO" in line:
                score -= 10000
            elif "OOO-" in line or "-OOO" in line:
                score -= 1000
            elif "OO-" in line or "-OO" in line or "O-O" in line:
                score -= 100
            return score

        lines = self.get_all_lines()
        total_score = 0
        for line in lines:
            line_str = "".join(line)
            total_score += eval_pos(line_str)
        return total_score


class SearchStrategy:
    def alpha_beta_search(self, problem, depth=2):
        def max_value(problem, alpha, beta, depth):
            if problem.is_goal
    
    


def play_game():
    problem = Problem()
    strategy = SearchStrategy()

    while True:
        problem.draw_board()
        if problem.current_player == problem.human_player:
            try:
                row, col = map(int, input("Enter your move (row col): ").split())
                if not (0 <= row < 8 and 0 <= col < 8) or not problem.make_move(
                    row, col, problem.human_player
                ):
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")
                continue
        else:
            print("Computer's turn...")
            move = strategy.alpha_beta_search(problem)
            if move:
                problem.make_move(move[0], move[1], problem.ai_player)
            else:
                print("No valid moves left for the computer.")

        if problem.check_winner(problem.human_player):
            problem.draw_board()
            print("Congratulations! You win!")
            break
        if problem.check_winner(problem.ai_player):
            problem.draw_board()
            print("Computer wins. Better luck next time!")
            break
        if problem.is_full():
            problem.draw_board()
            print("It's a draw!")
            break

        problem.switch_player()


if __name__ == "__main__":
    play_game()
p = Problem()
p.board[0][0] = "X"
p.board[1][1] = "X"
p.evaluate("X")
