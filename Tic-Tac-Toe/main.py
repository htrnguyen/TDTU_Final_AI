import os

from problem import Problem
from search import SearchStrategy

p = Problem()
s = SearchStrategy()

while not p.is_goal():
    os.system("cls" if os.name == "nt" else "clear")
    p.draw_board()

    if p.current_player == p.human_player:
        x, y = map(int, input("Enter your move (x y): ").split())
        while not p.make_move(x, y, p.human_player):
            print("Invalid move!", end=". ")
            x, y = map(int, input("Enter your move (x y): ").split())
    else:
        print("AI turn...")
        move = s.alpha_beta_search(p)
        p.make_move(*move, p.ai_player)
        print(f"AI move: {move}")

    p.current_player = (
        p.human_player if p.current_player == p.ai_player else p.ai_player
    )

    # Check if the game is over
    if p.is_goal():
        os.system("cls" if os.name == "nt" else "clear")
        p.draw_board()
        if p.check_winner(p.human_player):
            print("You win!")
        elif p.check_winner(p.ai_player):
            print("AI wins!")
        else:
            print("It's a draw!")
        break