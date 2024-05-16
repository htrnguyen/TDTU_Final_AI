import numpy as np


class Problem:
    def __init__(self, ai_player="X", human_player="O"):
        self.size = 8
        self.board = np.full((self.size, self.size), "·")
        self.ai_player = ai_player
        self.human_player = human_player
        self.current_player = self.human_player

    # Draw the board 8x8 in the console
    def draw_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            print(str(i) + " " + " ".join(self.board[i]))

    # Check if the move is valid
    def is_valid_move(self, move):
        x, y = move
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "·"

    # Make a move on the board
    def make_move(self, x, y, player):
        if self.is_valid_move((x, y)):
            self.board[x][y] = player
            return True
        return False

    # Undo a move on the board
    def undo_move(self, x, y):
        self.board[x][y] = "·"

    # Hash the board, ex: 123456789
    def hash_board(self):
        return hash(self.board.tostring())

    def switch_player(self):
        self.current_player = (
            self.ai_player
            if self.current_player == self.human_player
            else self.human_player
        )

    # Get all the lines on the board (rows, columns, diagonals)
    def get_all_lines(self):
        lines = []
        lines.extend(self.board.tolist())  # rows
        lines.extend(self.board.T.tolist())  # columns
        # diagonals
        for d in range(-self.size + 1, self.size):
            lines.append(np.diag(self.board, k=d).tolist())
            lines.append(np.diag(np.fliplr(self.board), k=d).tolist())

        lines = [line for line in lines if len(line) >= 4]
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
        return any(
            self.check_winner(p) for p in [self.ai_player, self.human_player]
        ) or not np.any(self.board == "·")

    # Get all possible moves
    def get_possible_moves(self):
        return [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == "·"
        ]

    def order_moves(self, maximum_player):
        moves = self.get_possible_moves()
        scores = []

        # Đánh giá mỗi nước đi
        for move in moves:
            self.make_move(*move, self.current_player)
            score = self.evaluate()
            scores.append((score, move))
            self.undo_move(*move)

        scores.sort(reverse=maximum_player)
        ordered_moves = [move for _, move in scores]
        return ordered_moves

    def evaluate(self):
        score = 0
        lines = self.get_all_lines()

        for line in lines:
            score += self.evaluate_line(line, self.ai_player)
            score -= self.evaluate_line(line, self.human_player)

        return score

    def evaluate_line(self, line, player):
        """
        Đánh giá một dòng trong bàn cờ Tic-Tac-Toe 8x8, dựa vào người chơi để xác định điểm số.

        Args:
            line: Một dòng trên bàn cờ, được biểu diễn dưới dạng một chuỗi các ký tự 'X', 'O' và '.'.
            player: Người chơi hiện tại, 'X' hoặc 'O'.

        Returns:
            Điểm số của dòng cho người chơi hiện tại.
        """

        # Điểm số cho các chuỗi tấn công, phòng thủ và chặn.
        SCORE_4 = 1000
        SCORE_3 = 800
        SCORE_2 = 500
        
        SCORE_4_BLOCK = 800
        SCORE_3_BLOCK = 500
        SCORE_2_BLOCK = 300

        # Điểm cho việc chiếm trung tâm dựa trên vị trí quân địch
        SCORE_CENTER_WITH_ENEMY_NEARBY = 50

        # Xác định ký hiệu của AI và người chơi
        ai_symbol = self.ai_player
        human_symbol = self.human_player

        # Tạo từ điển điểm số cho các chuỗi
        attack_dict = {
            ai_symbol * 4: SCORE_4,  # XXXX
            ai_symbol * 3 + "·": SCORE_3,  # XXX·
            ai_symbol * 2 + "·" + ai_symbol: SCORE_2,  # XX·X
            ai_symbol + "·" + ai_symbol * 2: SCORE_2,  # X·XX
            "·" + ai_symbol * 3: SCORE_3,  # ·XXX
            ai_symbol * 2 + "··": SCORE_2,  # XX··
            ai_symbol + "·" + ai_symbol + "·": SCORE_2,  # X·X·
            "·" + ai_symbol * 2 + "·": SCORE_2,  # ·XX·
        }

        defense_dict = {
            human_symbol * 4: SCORE_4_BLOCK,  # OOOO
            human_symbol * 3 + "·": SCORE_3_BLOCK,  # OOO·
            human_symbol * 2 + "·" + human_symbol: SCORE_2_BLOCK,  # OO·O
            human_symbol + "·" + human_symbol * 2: SCORE_2_BLOCK,  # O·OO
            "·" + human_symbol * 3: SCORE_3_BLOCK,  # ·OOO
            human_symbol * 2 + "··": SCORE_2_BLOCK,  # OO··
            human_symbol + "·" + human_symbol + "·": SCORE_2_BLOCK,  # O·O·
            "·" + human_symbol * 2 + "·": SCORE_2_BLOCK,  # ·OO·
        }

        block_dict = {
            ai_symbol + human_symbol * 3: SCORE_4_BLOCK,  # XOOO
            human_symbol * 3 + ai_symbol: SCORE_4_BLOCK,  # OOOX
            ai_symbol + human_symbol * 2 + "·": SCORE_3_BLOCK,  # XOO·
            ai_symbol + "·" + human_symbol * 2: SCORE_3_BLOCK,  # X·OO
            human_symbol * 2 + ai_symbol + "·": SCORE_3_BLOCK,  # OO·X
            "·" + ai_symbol + human_symbol * 2: SCORE_3_BLOCK,  # ·XOO
            ai_symbol + "·" + human_symbol + "·" + ai_symbol: SCORE_3_BLOCK,  # X·XO
            ai_symbol + human_symbol + "·" + ai_symbol + "·": SCORE_3_BLOCK,  # XO·X
            ai_symbol + "·" + human_symbol + ai_symbol + "·": SCORE_3_BLOCK,  # X·OX
            ai_symbol + "·" + ai_symbol + human_symbol + "·": SCORE_3_BLOCK,  # X·XO
            ai_symbol + "·" + ai_symbol + "·" + human_symbol: SCORE_3_BLOCK,  # X·XO
            "·" + ai_symbol + "·" + human_symbol + ai_symbol: SCORE_3_BLOCK,  # ·XOX
            "·" + ai_symbol + human_symbol + "·" + ai_symbol: SCORE_3_BLOCK,  # ·XOX
            ai_symbol + human_symbol + "·" + "·" + ai_symbol: SCORE_3_BLOCK,  # XOX·
            ai_symbol + "·" + human_symbol + "·" + ai_symbol: SCORE_3_BLOCK,  # X·OX
            ai_symbol + "·" + ai_symbol + "·" + human_symbol: SCORE_3_BLOCK,  # X·XO
            ai_symbol + "·" + ai_symbol + human_symbol + "·": SCORE_3_BLOCK,  # XXO·
            ai_symbol + "·" + human_symbol + ai_symbol + "·": SCORE_3_BLOCK,  # X·OX
            
        }

        score = 0

        # Xét các chuỗi con 4 ô liên tiếp
        for i in range(len(line) - 3):
            sub_line = "".join(line[i : i + 4])

            if player == self.ai_player and sub_line in attack_dict:
                score += attack_dict[sub_line]
            elif player == self.human_player and sub_line in defense_dict:
                score += defense_dict[sub_line]
            elif sub_line in block_dict:
                score += block_dict[sub_line]

        # Thêm điểm cho các vị trí chiến lược
        for i, symbol in enumerate(line):
            if symbol == player:
                if i == 3:
                    score += SCORE_CENTER_WITH_ENEMY_NEARBY
                elif i == 4:
                    score += SCORE_CENTER_WITH_ENEMY_NEARBY // 2
                elif i == 5:
                    score += SCORE_CENTER_WITH_ENEMY_NEARBY // 4

        return score
