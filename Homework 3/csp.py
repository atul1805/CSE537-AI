###########################################
# you need to implement five funcitons here
###########################################
import random

import utils

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    game =  utils.game(filename)
    
    def recursiveBacktracking(game):
        # consistencyChecks is incremented every time before checking for completion
        game.consistencyChecks += 1
        if game.isAssignmentComplete():
            return True
        pos = game.getUnassignedPositions(first=True) # Only get the first empty cell
        x = pos[0][0]
        y = pos[0][1]

        validMoves = game.getValidMoves(x,y)
        for move in validMoves:
            game.sudokuBoard[x][y] = move
            result = recursiveBacktracking(game)
            if result is not None:
                return result
        game.sudokuBoard[x][y] = 0 # Failed assignment. Reset and return None.
        return

    if recursiveBacktracking(game):
        return (game.sudokuBoard,game.consistencyChecks)
    else:
        return ("Solution not reached",game.consistencyChecks)
    
def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    game =  utils.game(filename)
    
    def recursiveBacktrackingMRV(game):
        game.consistencyChecks += 1
        if game.isAssignmentComplete():
            return True

        pos = game.getUnassignedPositions()
        mrvPos = game.getMRVPos(pos) # Find the most constrained position
        x = pos[mrvPos][0]
        y = pos[mrvPos][1]
        
        moves = game.getValidMoves(x,y)
        
        # Determine the least constraining value
        constraintCount = list()
        for i in range(len(moves)):
            game.sudokuBoard[x][y] = moves[i]
            constraintCount.append((moves[i],game.getConstraintCount(x,y)))
        lcvMoves = sorted(constraintCount, key=lambda constraintCount:constraintCount[1],reverse = True)

        # Backtrack
        for move in lcvMoves:
            game.sudokuBoard[x][y] = move[0]
            result = recursiveBacktrackingMRV(game)
            if result is not None:
                return result
        game.sudokuBoard[x][y] = 0
        return

    if recursiveBacktrackingMRV(game):
        return (game.sudokuBoard,game.consistencyChecks)
    else:
        return ("Solution not reached",game.consistencyChecks)

    
def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    game =  utils.game(filename)

    def recursivebacktrackingMRVfwd(game):
        game.consistencyChecks += 1
        if game.isAssignmentComplete():
            return True

        pos = game.getUnassignedPositions()
        mrvPos = game.getMRVPos(pos) # Find the most constrained position
        x = pos[mrvPos][0]
        y = pos[mrvPos][1]
        
        moves = game.getValidMoves(x,y)
        
        # Determine the least constraining value
        constraintCount = list()
        for i in range(len(moves)):
            game.sudokuBoard[x][y] = moves[i]
            constraintCount.append((moves[i],game.getConstraintCount(x,y)))
        lcvMoves = sorted(constraintCount, key=lambda constraintCount:constraintCount[1],reverse = True)

        # Backtrack
        for move in lcvMoves:
            game.sudokuBoard[x][y] = move[0]
            if game.forwardChecking(x,y): # Perform forward checking
                result = recursivebacktrackingMRVfwd(game)
                if result is not None:
                    return result
        game.sudokuBoard[x][y] = 0
        return

    if recursivebacktrackingMRVfwd(game):
        return (game.sudokuBoard,game.consistencyChecks)
    else:
        return ("Solution not reached",game.consistencyChecks)

def backtrackingMRVcp(filename):
    ###
    # use backtracking + MRV + cp to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    game = utils.game(filename)

    def recursivebacktrackingMRVcp(game):
        game.consistencyChecks += 1
        if game.isAssignmentComplete():
            return True

        pos = game.getUnassignedPositions()
        mrvPos = game.getMRVPos(pos) # Find the most constrained position
        x = pos[mrvPos][0]
        y = pos[mrvPos][1]
        
        moves = game.getValidMoves(x,y)
        
        # Determine the least constraining value
        constraintCount = list()
        for i in range(len(moves)):
            game.sudokuBoard[x][y] = moves[i]
            constraintCount.append((moves[i],game.getConstraintCount(x,y)))
        lcvMoves = sorted(constraintCount, key=lambda constraintCount:constraintCount[1],reverse = True)

        # Backtrack
        for move in lcvMoves:
            game.sudokuBoard[x][y] = move[0]
            if game.arcConsistent(): # Verify arc consistency
                result = recursivebacktrackingMRVcp(game)
                if result is not None:
                    return result
        game.sudokuBoard[x][y] = 0
        return

    if recursivebacktrackingMRVcp(game):
        return (game.sudokuBoard,game.consistencyChecks)
    else:
        return ("Solution not reached",game.consistencyChecks)

def minConflict(filename):
    ###
    # use minConflict to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    game = utils.game(filename)
    maxSteps = 50000 # The maximum number of iterations
    
    # Find all empty cells. These are the CSP's variables.
    variables = [(i, j) for i in range(len(game.sudokuBoard))
                        for j in range(len(game.sudokuBoard))
                        if game.sudokuBoard[i][j] == 0]
    # Initial assignment
    for var in variables:
        game.sudokuBoard[var[0]][var[1]] = game.leastConflicting(*var)
    
    for i in range(maxSteps):
        game.consistencyChecks += 1
        if game.isAssignmentValid():
            return (game.sudokuBoard, game.consistencyChecks)
        # Choose one variable at random, and assign the least conflicting value
        var = random.choice(variables)
        game.sudokuBoard[var[0]][var[1]] = game.leastConflicting(*var)
    
    # Out of iterations. Could not reach a valid assignment.
    return ("Solution not reached", game.consistencyChecks)
