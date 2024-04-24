class Problem:
    def __init__(self, side=4):
        self.side = side
        self.is_possible_solution = False
        self.clauses = self.create_clauses()
        self.board = [[ False for _ in range(side)] for _ in range(side)]

    def get_clauses(self):
        return self.clauses
    
    def create_clauses(self):
        N = self.side
        clauses = []

        for i in range(N):
            row_clause = [(i * N + j + 1) for j in range(N)]
            clauses.append(row_clause)  # one row has at least one Queen

            for j1 in range(N):
                for j2 in range(j1 + 1, N):
                    clauses.append([-row_clause[j1], -row_clause[j2]])  # one row has at most one Queen
            col_clause = [(j * N + i + 1) for j in range(N)]
            clauses.append(col_clause)  # one column has at least one Queen

            for j1 in range(N):
                for j2 in range(j1 + 1, N):
                    clauses.append([-col_clause[j1], -col_clause[j2]])  # one column has at most one Queen

        for i in range(N):
            for j in range(N):
                for k in range(i + 1, N):
                    d = k - i
                    if j - d >= 0:
                        clauses.append([-(i * N + j + 1), -(k * N + j - d + 1)])
                    if j + d < N:
                        clauses.append([-(i * N + j + 1), -(k * N + j + d + 1)])
        return clauses

    def add_solution(self, solution):
        if solution != None:
            self.is_possible_solution = True

            for i in range(self.side):
                for j in range(self.side):
                    if solution[i*self.side + j] > 0:
                        self.board[i][j] = True
    
    def draw_board(self):
        if self.is_possible_solution == False:
            print('No possible solution.')
        else:
            for row in self.board:
                for tile in row:
                    if tile == True:
                        print('Q', end=' ')
                    else:
                        print('.', end=' ')
                print()
            print()