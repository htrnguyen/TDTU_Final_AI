import time


class SearchStrategy:
    def __init__(self):
        self.transposition_table = {}

    def alpha_beta_pruning(
        self,
        problem,
        depth,
        alpha,
        beta,
        maximizing_player,
    ):
        state_key = (problem.board.tobytes(), maximizing_player)

        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0 or problem.is_goal():
            return problem.evaluate(), None

        best_move = None
        moves = problem.get_possible_moves()

        if maximizing_player:
            max_eval = float("-inf")
            for move in moves:
                problem.make_move(*move, "x")
                eval, _ = self.alpha_beta_pruning(
                    problem, depth - 1, alpha, beta, False
                )
                problem.undo_move(*move)

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
                problem.make_move(*move, "o")
                eval, _ = self.alpha_beta_pruning(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                
            self.transposition_table[state_key] = min_eval, best_move
            return min_eval, best_move

    def alpha_beta_search(self, problem, limit_depth=10):
        best_move = None
        best_score = float("-inf") if problem.player_turn == "x" else float("inf")
        depth = 1

        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time >= 5:
                break

            score, move = self.alpha_beta_pruning(
                problem, depth, float("-inf"), float("inf"), True
            )

            if problem.player_turn == "x" and score > best_score:
                best_score = score
                best_move = move
            elif problem.player_turn == "o" and score < best_score:
                best_score = score
                best_move = move

            depth += 1
            if depth > limit_depth:
                break

        return best_move