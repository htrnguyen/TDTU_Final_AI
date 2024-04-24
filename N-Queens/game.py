from problem import Problem
from CNF import CNF

N = 0
while N < 4:
    N = int(input('Enter side of board game: '))

p = Problem(N)
cnf = CNF()

clauses = p.get_clauses()
cnf.add_clauses(clauses)
solution = cnf.get_solution()
p.add_solution(solution) 
p.draw_board()


