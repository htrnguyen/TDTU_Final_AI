import time


class SearchStrategy:
    def alpha_beat_search(
        self,
        problem,
        depth,
        alpha,
        beta,
        max_player=True,
    ):
        board_hash = problem.hash_board()
        if board_hash in problem.transposition_table:
            return problem.transposition_table[board_hash], None

        if depth == 0 or problem.is_goal():
            return problem.evaluate(), None

        best_move = None
        if max_player:
            max_value = float("-inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, "x")
                eval, _ = self.alpha_beat_search(problem, depth - 1, alpha, beta, False)
                problem.undo_move(*move)

                if eval > max_value:
                    max_value = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[board_hash] = max_value
            return max_value, best_move
        else:
            min_value = float("inf")
            for move in problem.get_possible_moves():
                problem.make_move(*move, "o")
                eval, _ = self.alpha_beat_search(problem, depth - 1, alpha, beta, True)
                problem.undo_move(*move)

                if eval < min_value:
                    min_value = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            problem.transposition_table[board_hash] = min_value
            return min_value, best_move

    def find_best_move(self, problem, depth=4):
        best_move = None
        best_value = float("-inf")

        for depth in range(1, depth + 1):
            value, move = self.alpha_beat_search(
                problem, depth, float("-inf"), float("inf"), True
            )
            if value > best_value:
                best_value = value
                best_move = move

            print(f"Depth: {depth} - Best value: {best_value} - Move: {best_move}")
        print(f"Best value: {best_value} - Move: {best_move} - Depth: {depth}")
        return best_move
