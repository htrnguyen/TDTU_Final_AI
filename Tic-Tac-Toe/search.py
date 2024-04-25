import time


class SearchStrategy:
    def alpha_beat_pruning(
        self,
        problem,
        depth,
        alpha,
        beta,
        maximizing_player,
    ):
        hash_board = problem.hash_board()
        if hash_board in problem.transposition_table:
            return problem.transposition_table[hash_board], None

        if depth == 0 or problem.is_goal():
            return problem.evaluate(), None

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")

            for move in problem.get_possible_moves():
                problem.make_move(*move, problem.ai_player)
                eval, _ = self.alpha_beat_pruning(
                    problem, depth - 1, alpha, beta, False
                )
                problem.undo_move(*move)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[hash_board] = max_eval
            return max_eval, best_move

        else:
            min_eval = float("inf")

            for move in problem.get_possible_moves():
                problem.make_move(*move, problem.human_player)
                eval, _ = self.alpha_beat_pruning(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[hash_board] = min_eval
            return min_eval, best_move

    def alpha_beta_search(self, problem, limit_depth=4):
        best_move = None
        best_value = float("-inf")

        for depth in range(1, limit_depth + 1):
            value, move = self.alpha_beat_pruning(
                problem, depth, float("-inf"), float("inf"), True
            )

            if value > best_value:
                best_value = value
                best_move = move

        # print(f"Best value: {best_value}, Move: {best_move}, Depth: {limit_depth}")
        return best_move
