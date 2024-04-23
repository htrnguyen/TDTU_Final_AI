from pysat.solvers import Glucose3 

class CNF:
    def __init__(self):
        self.solver = Glucose3()

    def add_clauses(self, clauses):
        for clause in clauses:
            self.solver.add_clause(clause)
    
    def get_solution(self):
        self.solver.solve()
        return self.solver.get_model()
    
    
