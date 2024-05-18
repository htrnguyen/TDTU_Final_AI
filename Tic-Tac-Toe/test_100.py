from board import Board
from problem import Problem
from search import SearchStrategy
import os, random

class Game:
    def __init__(self, ai_starts=False, size=8):
        self.board = Board(size)
        self.game = Problem(self.board)
        self.strategy = SearchStrategy()
        self.ai_starts = ai_starts

        if self.ai_starts:
            self.game.current_player = self.game.ai_player

    def play(self, number=1):
        if self.game.current_player == self.game.ai_player:
            first_move = random.choice(self.game.get_valid_moves())
            self.board.make_move(first_move[0], first_move[1], self.game.ai_player)
            self.game.switch_player()

        while not self.game.is_game_over():        
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Game {number}")
            self.board.draw()
            if self.game.current_player == self.game.human_player:
                print("Human Turn")
                move = self.strategy.alpha_beta_search(self.game)
                self.board.make_move(move[0], move[1], self.game.human_player)
                self.game.switch_player()
            else:
                print("AI Turn")
                move = self.strategy.alpha_beta_search(self.game)
                self.board.make_move(move[0], move[1], self.game.ai_player)
                self.game.switch_player()
                
        os.system('cls' if os.name == 'nt' else 'clear')
        self.board.draw()
        if self.game.check_winner(self.game.human_player):
            return "Human"
        elif self.game.check_winner(self.game.ai_player):
            return "AI"
        else:
            return "Draw"

            
            
def run_simulations(num_games, size=8):
    ai_wins = 0
    human_wins = 0
    draws = 0

    for i in range(num_games):
        game = Game(ai_starts=True, size=size)
        result = game.play(i + 1)
        if result == "AI":
            ai_wins += 1
        elif result == "Human":
            human_wins += 1
        else:
            draws += 1

    print(f"AI wins: {ai_wins}")
    print(f"Human wins: {human_wins}")
    print(f"Draws: {draws}")


if __name__ == "__main__":
    num_games = 10
    size = 8
    run_simulations(num_games, size)