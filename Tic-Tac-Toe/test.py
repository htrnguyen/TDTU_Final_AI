import os

from problem import Problem
from search import SearchStrategy


# Play the game
def play_game():
    game = Problem()
    search = SearchStrategy()

    while True:
        game.draw_board()

        if game.player_turn == "x":
            x, y = map(int, input("Enter your move: ").split())
            while not game.is_valid_move(x, y):
                x, y = map(int, input("Invalid move. Enter your move: ").split())
            game.make_move(x, y, "x")
        else:
            print("AI is thinking...")
            x, y = search.find_best_move(game)
            game.make_move(x, y, "o")
        game.player_turn = "o" if game.player_turn == "x" else "x"
        os.system("cls" if os.name == "nt" else "clear")

        if game.check_winner("x"):
            game.draw_board()
            print("You win!")
            break
        if game.check_winner("o"):
            game.draw_board()
            print("AI wins!")
            break
        if game.is_goal():
            game.draw_board()
            print("It's a draw!")
            break


play_game()
