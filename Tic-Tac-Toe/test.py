import os

import problem
import search

p = problem.Problem()
s = search.SearchStrategy()


def play_game():
    while not p.is_goal():
        p.draw_board()

        if p.player_turn == "x":
            print("AI is thinking...")
            move = s.alpha_beta_search(p, limit_depth=10)
            p.make_move(*move, "x")
        else:
            x, y = map(int, input("Enter your move (x y): ").split())
            while not p.make_move(x, y, "o"):
                x, y = map(int, input("Invalid move. Enter your move (x y): ").split())

        p.player_turn = "o" if p.player_turn == "x" else "x"

        os.system("cls" if os.name == "nt" else "clear")

    p.draw_board()
    if p.check_winner("x"):
        print("AI wins!")
    elif p.check_winner("o"):
        print("You win!")
    else:
        print("It's a draw!")


play_game()
