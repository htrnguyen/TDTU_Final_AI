'''
5
'''
class SearchStrategy:
    '''
    Chiến lược tìm kiếm
    '''
    def alpha_beta_pruning(self, game, max_depth=2):
        '''
        Alpha-beta pruning
        '''
        def max_value(game, alpha, beta, depth):
            '''
            Tìm giá trị lớn nhất
            '''
            if game.is_game_over() or depth >= max_depth:
                return game.evaluate()

            value = float("-inf")
            for move in game.sort_moves():
                game.board.make_move(move[0], move[1], game.ai_player)
                value = max(value, min_value(game, alpha, beta, depth + 1))
                game.board.undo_move(move[0], move[1])
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        def min_value(game, alpha, beta, depth):
            '''
            Tìm giá trị nhỏ nhất
            '''
            if game.is_game_over() or depth >= max_depth:
                return game.evaluate()

            value = float("inf")
            for move in game.sort_moves():
                game.board.make_move(move[0], move[1], game.human_player)
                value = min(value, max_value(game, alpha, beta, depth + 1))
                game.board.undo_move(move[0], move[1])
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        alpha = float("-inf")
        beta = float("inf")
        best_value = float("-inf")
        best_move = None

        for move in game.sort_moves():
            x, y = move
            game.board.make_move(x, y, game.ai_player)
            value = min_value(game, alpha, beta, 1)
            game.board.undo_move(x, y)
            if value > best_value:
                best_value = value
                best_move = move
                # print(f"Best move: {best_move}, value: {best_value}")
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        return best_move
    
    def alpha_beta_search(self, problem):
        best_move = None
        limit_depth = 2
        for depth in range(1, limit_depth + 1):
            best_move = self.alpha_beta_pruning(problem, depth)
        return best_move
    
