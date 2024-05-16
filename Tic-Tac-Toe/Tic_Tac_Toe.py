import copy

# Kích thước bàn cờ
BOARD_SIZE = 8

# Biểu diễn người chơi
PLAYER_X = 1
PLAYER_O = 2

# Biểu diễn ô trống
EMPTY = 0

# Số quân cần để thắng
WIN_COUNT = 4

# Bảng tra cứu
transposition_table = {}


def print_board(board):
    """
    Hàm in bàn cờ ra màn hình console.
    """
    for row in board:
        print(
            " ".join(
                [
                    "." if cell == EMPTY else "X" if cell == PLAYER_X else "O"
                    for cell in row
                ]
            )
        )


def check_win(board, player):
    """
    Kiểm tra xem người chơi 'player' đã thắng hay chưa.
    """

    # Kiểm tra hàng ngang và dọc
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - WIN_COUNT + 1):
            if all(board[i][j + k] == player for k in range(WIN_COUNT)):
                return True
            if all(board[j + k][i] == player for k in range(WIN_COUNT)):
                return True

    # Kiểm tra đường chéo chính
    for i in range(BOARD_SIZE - WIN_COUNT + 1):
        for j in range(BOARD_SIZE - WIN_COUNT + 1):
            if all(board[i + k][j + k] == player for k in range(WIN_COUNT)):
                return True

    # Kiểm tra đường chéo phụ
    for i in range(WIN_COUNT - 1, BOARD_SIZE):
        for j in range(BOARD_SIZE - WIN_COUNT + 1):
            if all(board[i - k][j + k] == player for k in range(WIN_COUNT)):
                return True

    return False


def get_valid_moves(board):
    """
    Lấy danh sách các nước đi hợp lệ.
    """
    moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                moves.append((i, j))
    return moves


def evaluate(board):
    """
    Hàm đánh giá trạng thái bàn cờ cho máy (O).
    """
    score = 0
    for player in (PLAYER_O, PLAYER_X):
        # Kiểm tra hàng ngang và dọc
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - WIN_COUNT + 1):
                count = sum(board[i][j + k] == player for k in range(WIN_COUNT))
                if count == WIN_COUNT:
                    score += 1000 if player == PLAYER_O else -1000
                elif count > 0:
                    score += count if player == PLAYER_O else -count
            for j in range(BOARD_SIZE - WIN_COUNT + 1):
                count = sum(board[j + k][i] == player for k in range(WIN_COUNT))
                if count == WIN_COUNT:
                    score += 1000 if player == PLAYER_O else -1000
                elif count > 0:
                    score += count if player == PLAYER_O else -count

        # Kiểm tra đường chéo chính
        for i in range(BOARD_SIZE - WIN_COUNT + 1):
            for j in range(BOARD_SIZE - WIN_COUNT + 1):
                count = sum(board[i + k][j + k] == player for k in range(WIN_COUNT))
                if count == WIN_COUNT:
                    score += 1000 if player == PLAYER_O else -1000
                elif count > 0:
                    score += count if player == PLAYER_O else -count

        # Kiểm tra đường chéo phụ
        for i in range(WIN_COUNT - 1, BOARD_SIZE):
            for j in range(BOARD_SIZE - WIN_COUNT + 1):
                count = sum(board[i - k][j + k] == player for k in range(WIN_COUNT))
                if count == WIN_COUNT:
                    score += 1000 if player == PLAYER_O else -1000
                elif count > 0:
                    score += count if player == PLAYER_O else -count

    return score


def alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    Thuật toán Alpha-Beta Pruning với bảng tra cứu.
    """
    # Kiểm tra xem trạng thái bàn cờ đã có trong bảng tra cứu hay chưa
    hash_key = tuple(map(tuple, board))
    if hash_key in transposition_table:
        entry = transposition_table[hash_key]
        if entry[0] >= depth:
            if entry[1] == "EXACT":
                return entry[2]
            elif entry[1] == "LOWERBOUND":
                alpha = max(alpha, entry[2])
            elif entry[1] == "UPPERBOUND":
                beta = min(beta, entry[2])
            if alpha >= beta:
                return entry[2]

    if depth == 0 or check_win(board, PLAYER_X) or check_win(board, PLAYER_O):
        return evaluate(board)

    if maximizing_player:
        max_eval = -float("inf")
        for move in get_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_O
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        # Lưu kết quả vào bảng tra cứu
        transposition_table[hash_key] = (
            depth,
            "EXACT" if max_eval <= alpha else "LOWERBOUND",
            max_eval,
        )
        return max_eval
    else:
        min_eval = float("inf")
        for move in get_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = PLAYER_X
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        # Lưu kết quả vào bảng tra cứu
        transposition_table[hash_key] = (
            depth,
            "EXACT" if min_eval >= beta else "UPPERBOUND",
            min_eval,
        )
        return min_eval


def get_computer_move(board, limit_depth):
    """
    Tìm kiếm nước đi tốt nhất cho máy sử dụng Alpha-Beta Pruning.
    """
    best_move = None
    best_score = -float("inf")
    for move in get_valid_moves(board):
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = PLAYER_O
        score = alpha_beta(new_board, limit_depth, -float("inf"), float("inf"), False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def main():
    """
    Hàm main để chạy trò chơi.
    """
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = PLAYER_X
    while True:
        print_board(board)

        if current_player == PLAYER_X:
            # Lượt của người chơi
            while True:
                try:
                    row, col = map(
                        int, input("Nhập tọa độ nước đi (hàng, cột): ").split(",")
                    )
                    if (
                        0 <= row < BOARD_SIZE
                        and 0 <= col < BOARD_SIZE
                        and board[row][col] == EMPTY
                    ):
                        board[row][col] = PLAYER_X
                        break
                    else:
                        print("Nước đi không hợp lệ. Vui lòng thử lại.")
                except ValueError:
                    print(
                        "Nhập sai định dạng. Vui lòng nhập hai số nguyên cách nhau bởi dấu phẩy."
                    )
        else:
            # Lượt của máy
            depth = 2  # Độ sâu tìm kiếm
            move = get_computer_move(board, depth)
            board[move[0]][move[1]] = PLAYER_O
            print("Máy đã đi:", move)

        # Kiểm tra chiến thắng
        if check_win(board, current_player):
            print_board(board)
            print(
                "Người chơi", "X" if current_player == PLAYER_X else "O", "chiến thắng!"
            )
            break

        # Kiểm tra hòa
        if all(cell != EMPTY for row in board for cell in row):
            print_board(board)
            print("Hòa!")
            break

        # Đổi lượt chơi
        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X


if __name__ == "__main__":
    main()
