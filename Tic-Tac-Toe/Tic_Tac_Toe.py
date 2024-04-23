import time

import numpy as np


class TicTacToe:
    def __init__(self, size=8):
        self.size = size
        self.board = np.full((size, size), "·")
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
            self.board == "·"
        )

    def get_possible_moves(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == "·"
        ]

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

    def heuristic(self, move):
        self.board[move[0], move[1]] = self.player_turn
        score = self.evaluate()
        self.board[move[0], move[1]] = "·"
        return score

    def minimax(self, depth, alpha, beta, maximizing_player):
        state_key = (self.board.tobytes(), maximizing_player)

        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0 or self.is_terminal():
            return self.evaluate(), None

        best_move = None
        moves = self.get_possible_moves()

        if maximizing_player:
            max_eval = float("-inf")
            for move in moves:
                self.board[move[0], move[1]] = "x"
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[move[0], move[1]] = "·"

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            self.transposition_table[state_key] = max_eval, best_move
            return max_eval, best_move

        else:
            min_eval = float("inf")
            for move in moves:
                self.board[move[0], move[1]] = "o"
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[move[0], move[1]] = "·"

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            self.transposition_table[state_key] = min_eval, best_move
            return min_eval, best_move

    def iterative_deepening(self, limit_depth):
        best_move = None
        best_score = float("-inf") if self.player_turn == "x" else float("inf")
        depth = 1

        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time >= 5:
                break

            temp_score, temp_move = self.minimax(
                depth, float("-inf"), float("inf"), True
            )

            if self.player_turn == "x" and temp_score > best_score:
                best_score = temp_score
                best_move = temp_move
            elif self.player_turn == "o" and temp_score < best_score:
                best_score = temp_score
                best_move = temp_move

            # print(
            #     f"Depth: {depth}, Best move: {best_move}, Best score: {best_score}, Time: {current_time - start_time}"
            # )
            depth += 1

            if depth > limit_depth:
                break
        print("Best move:", best_move, "Best score:", best_score)
        return best_move


def play_game():
    game = TicTacToe(size=8)
    while not game.is_terminal():
        game.draw_board()

        if game.player_turn == "x":
            print("AI is thinking...")
            move = game.iterative_deepening(10)
            game.make_move(move[0], move[1], "x")
        else:
            print("Enter your move:", end=" ")
            valid_move = False
            while not valid_move:
                x, y = map(int, input().split())
                valid_move = game.make_move(x, y, "o")
                if not valid_move:
                    print("Invalid move. Try again.")
        game.player_turn = "o" if game.player_turn == "x" else "x"

    game.draw_board()
    if game.check_winner("x"):
        print("AI wins!")
    elif game.check_winner("o"):
        print("You win!")
    else:
        print("It's a draw!")


play_game()
# game = TicTacToe(size=5)
# print(game.minimax(3, float("-inf"), float("inf"), True))
