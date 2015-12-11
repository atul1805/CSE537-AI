import random

import readGame

class game:

    def __init__(self,filename):
        (self.sudokuBoard,self.N,self.M,self.K) = readGame.readGameState(filename)
        self.consistencyChecks = 0

    def isAssignmentComplete(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.sudokuBoard[i][j] == 0:
                    return False
        return True
    
    def isAssignmentValid(self):
        # Compare against the set representing a complete and valid assignment
        completeSet = set(range(1, self.N + 1))
        # Check whether rows and columns are valid
        for row in self.sudokuBoard:
            if set(row) != completeSet:
                return False
        for col in zip(*self.sudokuBoard): # Transpose sudokuBoard to check cols
            if set(col) != completeSet:
                return False
        # Check whether subgrids are valid
        for i in range(0, self.N, self.M):
            for j in range(0, self.N, self.K):
                subgrid = []
                for row in range(i, i + self.M):
                    subgrid.extend(self.sudokuBoard[row][j:j + self.K])
                if set(subgrid) != completeSet:
                    return False
        return True

    def getUnassignedPositions(self, first=False):
        pos = list()
        for i in range(self.N):
            for j in range(self.N):
                if self.sudokuBoard[i][j] == 0:
                    pos.append((i,j))
                    if first: # Only first position is needed; stop early.
                        return pos
        return pos

    def getAffectedCells(self,x,y):
        cells = set()
        # Cells in the same row or column
        for i in range(self.N):
            cells.add((x,i))
            cells.add((i,y))
        # Cells in the same subgrid
        subGrid_x = (x//self.M)*self.M;
        subGrid_y = (y//self.K)*self.K;
        for i in range(self.M):
            for j in range(self.K):
                cells.add((subGrid_x + i,subGrid_y + j))
        return list(cells)

    # Test for validity of value at x,y with respect to cells
    def isValidMove(self,x,y,cells):
        for cell in cells:
            if not (cell[0] == x and cell[1] == y): # Don't compare against self
                if self.sudokuBoard[cell[0]][cell[1]] == self.sudokuBoard[x][y]:
                    return False
        return True

    def getValidMoves(self,x,y):
        cells = self.getAffectedCells(x,y)
        moves = list()
        oldVal = self.sudokuBoard[x][y] # Save cell value; will be overwritten
        for move in range(1,self.N+1):
            self.sudokuBoard[x][y] = move
            if self.isValidMove(x,y,cells):
                moves.append(move)
        self.sudokuBoard[x][y] = oldVal # Restore the original cell value
        return moves

    # Search pos and find the cell with the minimum remaining values (valid moves)
    def getMRVPos(self,pos):
        minCount = self.N + 1
        mrvPos = 0
        for i in range(len(pos)):
            count = len(self.getValidMoves(pos[i][0],pos[i][1]))
            if minCount > count:
                minCount = count
                mrvPos = i
        return mrvPos

    # Get total number of valid moves for all "neighbors" of x,y
    def getConstraintCount(self,x,y):
        count = 0
        cells = self.getAffectedCells(x,y)
        for cell in cells:
            if not (cell[0] == x and cell[1] == y):
                count += len(self.getValidMoves(cell[0],cell[1]))
        return count

    # Check whether each "neighbor" of x,y has at least one remaining value
    def forwardChecking(self,x,y):
        cells = self.getAffectedCells(x,y)
        for cell in cells:
            if not (cell[0] == x and cell[1] == y):
                if (len(self.getValidMoves(cell[0],cell[1])) == 0):
                    return False
        return True
    
    # Is this board arc consistent?
    def arcConsistent(self):
        empty = self.getUnassignedPositions()
        # Enumerate domains and build queue
        domains = {}
        queue = []
        for pos in empty:
            domains[pos] = self.getValidMoves(*pos)
            queue.extend([(other, pos) for other in self.getAffectedCells(*pos)
                          if other in empty and other != pos]) # Add neighbors to queue
        
        while queue:
            pos1, pos2 = queue.pop(0)
            if (len(domains[pos1]) == 0) or (len(domains[pos2]) == 0):
                return False
            if len(domains[pos2]) == 1: # always consistent if there's more than one choice
                if domains[pos2][0] in domains[pos1]:
                    domains[pos1].remove(domains[pos2][0])
                    queue.extend([(pos2, pos1) for pos2 in self.getAffectedCells(*pos1)
                                  if pos2 in domains and pos2 != pos1]) # Add neighbors to queue
        return True
    
    def numConflicts(self, x, y):
        conflicts = 0
        value = self.sudokuBoard[x][y] # Save original value
        self.sudokuBoard[x][y] = 0
        
        # Row and column conflicts
        if value in self.sudokuBoard[x]:
            conflicts += 1
        if value in zip(*self.sudokuBoard)[y]: # Transposed sudokuBoard
            conflicts += 1
        
        # Subgrid conflicts
        sx = (x // self.M) * self.M
        sy = (y // self.K) * self.K
        subgrid = []
        for row in range(sx, sx + self.M):
            subgrid.extend(self.sudokuBoard[row][sy:sy + self.K])
        if value in subgrid:
            conflicts += 1
        
        self.sudokuBoard[x][y] = value # Restore original
        return conflicts
    
    def leastConflicting(self, x, y):
        original = self.sudokuBoard[x][y] # Save original value
        
        # Enumerate conflicts for each move
        conflictCount = {}
        for value in range(1, self.N + 1):
            self.sudokuBoard[x][y] = value
            conflictCount[value] = self.numConflicts(x, y)
        
        # Find least conflicting move
        _, minAmount = min(conflictCount.iteritems(), key=lambda (k, v): v)
        minimalMoves = [k for k, v in conflictCount.iteritems() if v == minAmount]
        value = random.choice(minimalMoves) # Break tie randomly
        
        self.sudokuBoard[x][y] = original # Restore original value
        return value
