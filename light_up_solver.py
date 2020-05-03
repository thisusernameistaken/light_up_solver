from z3 import *

"""
https://www.puzzle-light-up.com/?pl=5c87ce76b71cd1caab7d0873127972055d728be72f240
-1 : empty square
-2 : black square
>=0 : black numbered square

sym_board
 0 : black
 1 : light
 2 : light bulb
"""

class LightSolver:

    def __init__(self,board):
        self.board = board
        self.sym_board = []
        self.solver = Solver()
    
    def solve_puzzle(self):
        # Build Symolic board
        for row in range(len(self.board)):
            r = []
            for col in range(len(self.board)):
                r.append(BitVec('r%ic%i'%(row,col),8))
            self.sym_board.append(r)

        # Populate Symbolic board
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                # Valid options
                self.solver.add(And(self.sym_board[row][col] >=0, self.sym_board[row][col] <=2))
                
                # Sight rule
                sight = self.in_sight(row,col)
                for s in sight:
                    self.solver.add(If(self.sym_board[row][col] == 2, s==1,s!=3))
                
                # Has to have a lightbuld if lit
                self.solver.add(If(self.sym_board[row][col] == 1,
                    Sum([If(i == 2, 1,0) for i in self.in_sight(row,col)]) > 0,
                    self.sym_board[row][col] != -10))
                
                # filled piece
                if self.board[row][col] == -2:
                    self.solver.add(self.sym_board[row][col] == 0)
                # numbered piece
                elif self.board[row][col] >= 0:
                    self.solver.add(self.sym_board[row][col] == 0)
                    neighbors = self.get_neighbors(row,col)
                    self.count(2,neighbors,self.board[row][col])
                # Empty piece    
                elif self.board[row][col] == -1:
                    neighbors = self.get_neighbors(row,col)
                    if len(neighbors) == 0:
                        self.solver.add(self.sym_board[row][col] == 2)
                    else:
                        self.solver.add(self.sym_board[row][col] != 0)
        self.print_board()

    def in_sight(self,row,col):
        sight = []
        # Forward
        for r in range(row+1,len(self.board)):
            if self.board[r][col] == -1:
                sight.append(self.sym_board[r][col])
            else:
                break
        # Backard
        for r in range(row-1,-1,-1):
            if self.board[r][col] == -1:
                sight.append(self.sym_board[r][col])
            else:
                break
        # Up
        for c in range(col-1,-1,-1):
            if self.board[row][c] == -1:
                sight.append(self.sym_board[row][c])
            else:
                break
        # Down
        for c in range(col+1,len(self.board)):
            if self.board[row][c] == -1:
                sight.append(self.sym_board[row][c])
            else:
                break
        return sight
        
    def count(self,value,x,n):
        self.solver.add(n == Sum([If(x[i] == value, 1,0) for i in range(len(x))]))

    def is_empty(self,row,col):
        return self.board[row][col] == -1

    def get_neighbors(self,row,col):
	n = []
	if row+1 < len(self.board) and self.is_empty(row+1,col):
		n.append(self.sym_board[row+1][col])
	if row-1 >-1 and self.is_empty(row-1,col):
		n.append(self.sym_board[row-1][col])
        if col+1 < len(self.board) and self.is_empty(row,col+1):
		n.append(self.sym_board[row][col+1])
	if col-1 >-1 and self.is_empty(row,col-1):
		n.append(self.sym_board[row][col-1])
        return n

    def print_board(self):
        if self.solver.check():
            m = self.solver.model()
            for row in self.sym_board:
                for cell in row:
                    print str(m[cell]) + " | ",
                print ("\n"+"____"*(len(self.board)+1))


if __name__ == '__main__':
    
    board = [[-1,-1,-1,-1,-2,-1,-1],
             [-1, 3, 1,-1,-1, 2,-1],
             [-2,-1,-1,-1,-1, 0,-1],
             [-1,-1,-1,-1,-1,-1,-1],
             [-1, 1,-1,-1,-1,-1,-2],
             [-1, 0,-1,-1,-2, 2,-1],
             [-1,-1,-2,-1,-1,-1,-1]]
    
    board = [[-1,-2,-1,-1,-1, 3,-1],
             [ 1,-1,-1,-1, 2,-1,-2],
             [-1, 1,-1,-1,-1,-1,-1],
             [-1,-1,-1,-1,-1,-1,-1],
             [-1,-1,-1,-1,-1, 2,-1],
             [-2,-1,-2,-1,-1,-1,-2],
             [-1, 2,-1,-1,-1,-2,-1]]
    
    board = [[-1,-1,-1,-1, 2,-1,-1],
             [-1,-1,-1, 3,-1,-1,-1],
             [ 2,-1,-2,-1, 2,-1,-1],
             [-1,-2,-1,-2,-1, 1,-1],
             [-1,-1,-2,-1,-2,-1,-2],
             [-1,-1,-1,-2,-1,-1,-1],
             [-1,-1, 3,-1,-1,-1,-1]]
    
    board = [[-1,-1,-1,-1, 0,-1,-1],
             [-1,-1, 1,-1,-1,-1,-1],
             [ 2,-1,-1,-2,-1, 3,-1],
             [-1,-1,-2,-1,-2,-1,-1],
             [-1, 0,-1,-2,-1,-1, 1],
             [-1,-1,-1,-1,-2,-1,-1],
             [-1,-1, 3,-1,-1,-1,-1]]

    s = LightSolver(board)
    s.solve_puzzle()
