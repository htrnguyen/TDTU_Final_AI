import os

from problem import Problem
from search import SearchStrategy

p = Problem()
s = SearchStrategy()

while not p.is_goal():
    p.draw_board()
    if p.current_player == p.human_player:
        x, y = map(int, input("Enter your move (x y): ").strip().split())
        while not p.make_move(x, y, p.human_player):
            print("Invalid move! Try again.")
            x, y = map(int, input("Enter your move (x y): ").strip().split())
    else:
        move = s.alpha_beta_search(p)
        p.make_move(*move, p.ai_player)
        print(f"AI move: {move}")
    p.switch_player()
    # os.system("cls" if os.name == "nt" else "clear") 

if p.check_winner(p.human_player):
    p.draw_board()
    print("You win!")
elif p.check_winner(p.ai_player):
    p.draw_board()
    print("AI wins!")
else:
    p.draw_board()
    print("It's a draw!")
