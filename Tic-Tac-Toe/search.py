import time


class SearchStrategy:
    def alpha_beta_pruning(self, problem, depth, alpha, beta, maximizing_player):
        if depth == 0 or problem.is_goal():
            return problem.evaluate(), None

        moves = problem.order_moves(maximizing_player)
        best_move = None
        for move in moves:
            problem.make_move(*move, problem.current_player)
            eval, _ = self.alpha_beta_pruning(
                problem, depth - 1, alpha, beta, not maximizing_player
            )
            problem.undo_move(*move)
            
            if maximizing_player:
                if eval > alpha:
                    alpha = eval
                    best_move = move
            else:
                if eval < beta:
                    beta = eval
                    best_move = move
                    
            if alpha >= beta:
                break
        if maximizing_player:
            return alpha, best_move
        else:
            return beta, best_move

    def alpha_beta_search(self, problem, max_depth=2):
        best_eval = float("-inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        for depth in range(1, max_depth + 1):
            start_time = time.time()
            eval, move = self.alpha_beta_pruning(problem, depth, alpha, beta, True)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            end_time = time.time() - start_time
            print(
                f"Depth: {depth}, Time: {end_time:.2f}, Best Eval: {best_eval}, Best Move: {best_move}"
            )
        return best_move
