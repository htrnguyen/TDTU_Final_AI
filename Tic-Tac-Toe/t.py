import os

# Define the size of the board
BOARD_SIZE = 8


# Initialize the board with empty spaces
def create_board():
    return [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


# Print the current state of the board
def print_board(board):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for idx, row in enumerate(board):
        print(str(idx) + " " + "|".join(row))
        if idx < BOARD_SIZE - 1:
            print("  " + "-" * (BOARD_SIZE * 2 - 1))


# Check if the move by the player is valid
def is_valid_move(board, x, y):
    return x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE and board[x][y] == " "


# Place a move on the board
def place_move(board, x, y, player):
    valid = is_valid_move(board, x, y)
    if valid:
        board[x][y] = player
    return valid


# Check for a win condition on the board
def check_winner(board, player):
    # Horizontal, vertical, and diagonal checks
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if y <= BOARD_SIZE - 4 and all(board[x][y + i] == player for i in range(4)):
                return True
            if x <= BOARD_SIZE - 4 and all(board[x + i][y] == player for i in range(4)):
                return True
            if (
                x <= BOARD_SIZE - 4
                and y <= BOARD_SIZE - 4
                and all(board[x + i][y + i] == player for i in range(4))
            ):
                return True
            if (
                x >= 3
                and y <= BOARD_SIZE - 4
                and all(board[x - i][y + i] == player for i in range(4))
            ):
                return True
    return False


# Implementing suggested optimizations including an advanced evaluation function, iterative deepening, and enhanced alpha-beta pruning


def advanced_evaluate_board(board, player):
    score = 0
    opponent = 'X' if player == 'O' else 'O'
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # right, down, down-right, down-left
    
    def count_sequence(x, y, dx, dy, count_player):
        count = 0
        open_ends = 0
        for i in range(4):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if board[nx][ny] == count_player:
                    count += 1
                elif board[nx][ny] == ' ':
                    open_ends += 1
                else:
                    break
            else:
                break
        return count, open_ends

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            for dx, dy in directions:
                if board[x][y] == ' ':
                    # Potential score if player moves here
                    count, open_ends = count_sequence(x, y, dx, dy, player)
                    if count == 3 and open_ends > 0:
                        score += 100  # Winning move
                    elif count == 2 and open_ends == 2:
                        score += 10  # Open two

                    # Potential loss if opponent moves here
                    count, open_ends = count_sequence(x, y, dx, dy, opponent)
                    if count == 3 and open_ends > 0:
                        score -= 100  # Blocking opponent winning move

    return score



def evaluate_position(board, x, y, dx, dy, player):
    # Count connected pieces and open ends
    count = 0
    open_ends = 0
    for i in range(4):
        nx, ny = x + dx * i, y + dy * i
        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[nx][ny] == player:
                count += 1
            elif board[nx][ny] == " ":
                open_ends += 1
            else:
                break
        else:
            break
    # Scoring logic for the evaluated position
    if count == 4:
        return 1000  # Immediate winning condition
    elif count == 3 and open_ends > 0:
        return 100  # Open three: Potential to win
    elif count == 2 and open_ends == 2:
        return 10  # Open two: Less immediate threat
    return 0


# Enhancing alpha-beta pruning with move ordering and advanced evaluation
def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or check_winner(board, "X") or check_winner(board, "O"):
        return advanced_evaluate_board(board, player), None

    best_move = None
    if maximizing_player:
        max_eval = float("-inf")
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == " ":
                    board[x][y] = player
                    eval, _ = alpha_beta_pruning(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False,
                        "X" if player == "O" else "O",
                    )
                    board[x][y] = " "
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (x, y)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == " ":
                    board[x][y] = player
                    eval, _ = alpha_beta_pruning(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True,
                        "X" if player == "O" else "O",
                    )
                    board[x][y] = " "
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (x, y)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return min_eval, best_move


# Test function to check the overall integration of these changes
def test_game():
    board = create_board()
    player = "X"
    game_over = False
    max_depth = 3  # Adjust depth based on testing needs

    while not game_over:
        print_board(board)
        if player == "X":
            x, y = map(int, input("Enter your move (x y): ").strip().split())
            if is_valid_move(board, x, y):
                place_move(board, x, y, player)
            player = "O"
        else:
            print("Computer's turn...")
            _, best_move = alpha_beta_pruning(
                board, max_depth, float("-inf"), float("inf"), True, player
            )
            if best_move:
                place_move(board, best_move[0], best_move[1], player)
            player = "X"

        if (
            check_winner(board, "X")
            or check_winner(board, "O")
            or all(all(cell != " " for cell in row) for row in board)
        ):
            game_over = True

    print_board(board)
    print("Game over!")
    return "Test complete."


# Prepare this updated code for user download or testing within an appropriate Python environment
# Note: Uncomment the test_game() call in an appropriate environment to see these changes in action.
test_game()
