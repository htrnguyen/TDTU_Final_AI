class SearchStrategy:
    """
    Chiến lược tìm kiếm sử dụng thuật toán Alpha-Beta Pruning
    """

    def __init__(self, max_depth=1):
        self.max_depth = max_depth

    def alpha_beta_search(self, problem):
        """
        Tìm kiếm nước đi tốt nhất cho AI sử dụng thuật toán Alpha-Beta Pruning
        """

        def max_value(problem, alpha, beta, depth):
            if problem.is_game_over() or depth >= self.max_depth:
                return problem.evaluate()

            value = float("-inf")
            for move in problem.sort_moves():
                problem.board.make_move(*move, problem.ai_player)
                value = max(value, min_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(*move)

                if value >= beta:
                    return value
                alpha = max(alpha, value)

            return value

        def min_value(problem, alpha, beta, depth):
            if problem.is_game_over() or depth >= self.max_depth:
                return problem.evaluate()

            value = float("inf")
            for move in problem.sort_moves():
                problem.board.make_move(*move, problem.human_player)
                value = min(value, max_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(*move)

                if value <= alpha:
                    return value
                beta = min(beta, value)

            return value

        best_move = None
        best_value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for move in problem.sort_moves():
            problem.board.make_move(*move, problem.ai_player)
            value = min_value(problem, alpha, beta, 0)
            problem.board.undo_move(*move)

            if value > best_value:
                best_value = value
                best_move = move
                # print(f"Move: {move}, Value: {value}")
            alpha = max(alpha, best_value)

        return best_move
