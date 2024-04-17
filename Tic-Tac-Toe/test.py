import os

from problem import Problem
from search import SearchStrategy


def play_game():
    p = Problem()
    strategy = SearchStrategy()

    while not p.game_over():

        os.system("cls" if os.name == "nt" else "clear")

        p.draw_board()
        if p.player_turn == "X":
            # Player X's turn (Human)
            try:
                x, y = map(int, input("Enter your move (x y): ").strip().split())
                while not p.is_valid_move(x, y):
                    print("Invalid move. Try again.")
                    x, y = map(int, input("Enter your move (x y): ").strip().split())
            except ValueError:
                print("Please enter valid integer coordinates.")
                continue
            p.place_move(x, y)
        else:
            # Player O's turn (Computer)
            x, y = strategy.alpha_beta_search(p)
            if x is not None and y is not None:
                p.place_move(x, y)
            else:
                print("No valid moves left for the computer.")

    p.draw_board()
    winner = p.check_winner()
    if winner is None:
        print("It's a draw.")
    else:
        print(f"Player {winner} wins.")


if __name__ == "__main__":
    play_game()
