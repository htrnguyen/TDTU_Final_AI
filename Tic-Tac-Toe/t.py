class Problem:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.player_turn = 'X'

    def is_terminal(self):
        # Kiểm tra điều kiện kết thúc trò chơi: chiến thắng hoặc hòa
        if any(self.check_winner(player) for player in 'XO'):
            return True
        if all(self.board[row][col] != ' ' for row in range(8) for col in range(8)):
            return True
        return False

    def check_winner(self, player):
        # Kiểm tra xem có 4 quân liên tiếp của `player` không
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == player:
                    for dr, dc in directions:
                        if self.check_line(player, row, col, dr, dc, 4):
                            return True
        return False

    def check_line(self, player, row, col, dr, dc, count):
        for i in range(1, count):
            r, c = row + dr * i, col + dc * i
            if r < 0 or r >= 8 or c < 0 or c >= 8 or self.board[r][c] != player:
                return False
        return True

    def get_actions(self):
        # Lấy danh sách các nước đi hợp lệ (chưa được đánh)
        return [(r, c) for r in range(8) for c in range(8) if self.board[r][c] == ' ']

    def result(self, action):
        # Trả về bảng mới sau khi thực hiện nước đi
        new_board = [row[:] for row in self.board]
        new_board[action[0]][action[1]] = self.player_turn
        return new_board

    def utility(self):
        # Đánh giá trạng thái của bảng
        if self.check_winner('X'):
            return float('inf')  # X thắng
        elif self.check_winner('O'):
            return float('-inf')  # O thắng
        else:
            return 0  # Hòa

class SearchStrategy:
    def alpha_beta_search(self, problem):
        # Thuật toán alpha-beta pruning
        def max_value(board, alpha, beta, depth):
            if depth == 0 or problem.is_terminal():
                return problem.utility()
            v = float('-inf')
            for action in problem.get_actions():
                v = max(v, min_value(problem.result(action), alpha, beta, depth-1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(board, alpha, beta, depth):
            if depth == 0 or problem.is_terminal():
                return problem.utility()
            v = float('inf')
            for action in problem.get_actions():
                v = min(v, max_value(problem.result(action), alpha, beta, depth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        beta = float('inf')
        best_action = None
        for action in problem.get_actions():
            value = min_value(problem.result(action), best_score, beta, 3)  # Giả sử độ sâu là 3
            if value > best_score:
                best_score = value
                best_action = action
        return best_action

class Game:
    def __init__(self):
        self.problem = Problem()
        self.strategy = SearchStrategy()

    def play(self):
        while not self.problem.is_terminal():
            print(self.problem.board)
            if self.problem.player_turn == 'X':
                row, col = map(int, input("Enter row and column for X: ").split())
                self.problem.board[row][col] = 'X'
                self.problem.player_turn = 'O'
            else:
                action = self.strategy.alpha_beta_search(self.problem)
                self.problem.board[action[0]][action[1]] = 'O'
                self.problem.player_turn = 'X'

game = Game()
game.play()
