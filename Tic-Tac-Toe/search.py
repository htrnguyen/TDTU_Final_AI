class SearchStrategy:
    def __init__(self, max_depth=4):
        self.max_depth = max_depth

    def alpha_beta_search(self, p):
        def max_value(state, alpha, beta, depth):
            if p.game_over() or depth == 0:
                return p.utility(), None
            v = float("-inf")
            action = None
            for a in p.actions():
                min_v, _ = min_value(p.result(state, a), alpha, beta, depth - 1)
                if min_v > v:
                    v = min_v
                    action = a
                if v >= beta:
                    return v, action
                alpha = max(alpha, v)
            return v, action

        def min_value(state, alpha, beta, depth):
            if p.game_over() or depth == 0:
                return p.utility(), None
            v = float("inf")
            action = None
            for a in p.actions():
                max_v, _ = max_value(p.result(state, a), alpha, beta, depth - 1)
                if max_v < v:
                    v = max_v
                    action = a
                if v <= alpha:
                    return v, action
                beta = min(beta, v)
            return v, action

        _, action = max_value(
            p.get_state(), float("-inf"), float("inf"), self.max_depth
        )

        return action
