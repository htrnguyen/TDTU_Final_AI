class SearchStrategy:
    def alpha_beta_search(self, problem, max_depth=2):
        def max_value(problem, alpha, beta, depth):
            if problem.is_goal() or depth >= max_depth:
                return problem.evaluate()

            value = float("-inf")
            for move in problem.sort_moves():
                problem.board.make_move(move[0], move[1], problem.ai_player)
                value = max(value, min_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(move[0], move[1])
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        def min_value(problem, alpha, beta, depth):
            if problem.is_goal() or depth >= max_depth:
                return problem.evaluate()

            value = float("inf")
            for move in problem.sort_moves():
                problem.board.make_move(move[0], move[1], problem.human_player)
                value = min(value, max_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(move[0], move[1])
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        alpha = float("-inf")
        beta = float("inf")
        best_value = float("-inf")
        best_move = None

        for move in problem.sort_moves():
            problem.board.make_move(move[0], move[1], problem.ai_player)
            value = min_value(problem, alpha, beta, 1)
            problem.board.undo_move(move[0], move[1])
            if value > best_value:
                best_value = value
                best_move = move
                # print(f"Best move: {best_move}, value: {best_value}")
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        return best_move
