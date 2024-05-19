class SearchStrategy:
    """
    Chiến lược tìm kiếm sử dụng thuật toán Alpha-Beta Pruning
    """
    
    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def alpha_beta_pruning(self, problem, alpha, beta, depth):
        """
        Alpha-beta pruning
        """
        def max_value(problem, alpha, beta, depth):
            if depth >= self.max_depth or problem.is_game_over():
                return problem.evaluate()
            
            v = float("-inf")
            current_player = problem.current_player
            problem.current_player = problem.ai_player
            for move in problem.sort_moves():
                problem.board.make_move(*move, problem.ai_player)
                v = max(v, min_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(*move)
                if v >= beta:
                    problem.current_player = current_player
                    return v
                alpha = max(alpha, v)
            problem.current_player = current_player
            return v

        def min_value(problem, alpha, beta, depth):
            if depth >= self.max_depth or problem.is_game_over():
                return problem.evaluate()
            
            v = float("inf")
            current_player = problem.current_player
            problem.current_player = problem.human_player
            for move in problem.sort_moves():
                problem.board.make_move(*move, problem.human_player)
                v = min(v, max_value(problem, alpha, beta, depth + 1))
                problem.board.undo_move(*move)
                if v <= alpha:
                    problem.current_player = current_player
                    return v
                beta = min(beta, v)
            problem.current_player = current_player
            return v
        
        best_move = None
        v = float("-inf")
        current_player = problem.current_player
        for move in problem.sort_moves():
            problem.board.make_move(*move, problem.ai_player)
            move_value = min_value(problem, alpha, beta, 1)
            problem.board.undo_move(*move)
            if move_value > v:
                v = move_value
                best_move = move
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        problem.current_player = current_player
        return best_move
        
    def alpha_beta_search(self, problem):
        """
        Alpha-beta search
        """
        return self.alpha_beta_pruning(problem, float("-inf"), float("inf"), 0)
