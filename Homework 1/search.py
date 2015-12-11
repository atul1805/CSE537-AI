from copy import deepcopy
import math
import Queue
import config
import pegSolitaireUtils

# This function generates children gameState's for a given gameState.
# It accpets a parent object of class game and returns all possible child
# objects.
def children(parent,pegSolitaireObject):
    for i in range(7):
        for j in range(7):
            for direction in ['N','E','W','S']:
                if parent.is_validMove((i,j),direction):
                    child = deepcopy(parent)
                    AdjacentPos = child.getNextPosition((i,j),direction)
                    newPos = child.getNextPosition(AdjacentPos,direction)
                    child.getNextState((i,j),direction)
                    pegSolitaireObject.trace.append((i,j))
                    pegSolitaireObject.trace.append(newPos)
                    yield child


# This function determines whether a given gameState is goal or not
def GoalTest(gameState):
    goal = [[-1,-1,0, 0, 0,-1,-1],
            [-1,-1,0, 0, 0,-1,-1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [-1,-1,0, 0, 0,-1,-1],
            [-1,-1,0, 0, 0,-1,-1]]
    if gameState == goal:
        return True
    else:
        return False


def ItrDeepSearch(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    # 
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you 
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you 
    # reach goal using Iterative Deepning Search.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to save
    #
    #################################################
    
    # This function does a depth first search on a given gameState upto a given
    # depth to reach to the goal 
    def DepthLimitedSearch(parent,depth):
        if GoalTest(parent.gameState):
            return 1
        elif depth == 0:
            return
        elif depth > 0:
            # Generating children:
            for child in children(parent,pegSolitaireObject):
                childState = [tuple(i) for i in child.gameState]
                childState = tuple(childState)
                # Checking if given gameState has been visited or not:
                if childState not in visitedStates:
                    visitedStates.add(childState)
                    pegSolitaireObject.nodesExpanded += 1
                    # Recursively invoking search for the new child node:
                    result = DepthLimitedSearch(child,depth-1)
                    if result is not None:
                        return result
                    else:
                        pegSolitaireObject.trace.pop()
                        pegSolitaireObject.trace.pop()
                else:
                    pegSolitaireObject.trace.pop()
                    pegSolitaireObject.trace.pop()
            
            return
    
    maxDepth = 25 # Variable determining maximum depth to be explored
    for depth in range(0, maxDepth):
        visitedStates = set()
        result = DepthLimitedSearch(pegSolitaireObject,depth)
        if result is not None:
            return
    print "Solution Not Found"
    return


def aStarOne(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    # 
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you 
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you 
    # reach goal using A-Star searching with first Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    
    PQueue = Queue.PriorityQueue()
    
    # First Heuristic
    # The heuristic calculates the average distance of the pegs from the
    # centre(3,3). Lesser the distance nearer we are to the goal.
    def heuristic(node):
        distance = 0
        numOfPegs = 0
        for i in range(7):
            for j in range(7):
                if node.gameState[i][j] == 1:
                    distance = distance + math.sqrt((i-3)*(i-3) + (j-3)*(j-3))
                    numOfPegs = numOfPegs + 1

        return distance/numOfPegs
    
    # This function does a variation of breadth first search depending upon the
    # heuristics to select the next node from the PriorityQueue.
    def bfs(parent):
        PQueue.put((heuristic(parent),parent))
        while not PQueue.empty():
            node = PQueue.get()[1]
            if GoalTest(node.gameState):
                # Once goal found the trace is the current nodes trace:
                pegSolitaireObject.trace = node.trace
                return 1
            # Generating children:
            for child in children(node,pegSolitaireObject):
                childState = [tuple(i) for i in child.gameState]
                childState = tuple(childState)
                # Checking if children have been visted before:
                if childState not in visitedStates:
                    visitedStates.add(childState)
                    pegSolitaireObject.nodesExpanded += 1
                    newPos = pegSolitaireObject.trace.pop()
                    oldPos = pegSolitaireObject.trace.pop()
                    child.trace.append(oldPos)
                    child.trace.append(newPos)
                    PQueue.put((heuristic(child),child))
                else:
                    pegSolitaireObject.trace.pop()
                    pegSolitaireObject.trace.pop()
                
        return
    
    visitedStates = set()
    if bfs(pegSolitaireObject) is None:
        print "Solution Not Found"
    return    


def aStarTwo(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    # 
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you 
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you 
    # reach goal using A-Star searching with second Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    
    PQueue = Queue.PriorityQueue()
    
    # The heuristic calculates the number of isolated pegs in a given gameState.
    # Isolated Pegs are those pegs which cannot be moved out of the board by any
    # move in a given gamestate. Lesser is this count closer we are to the goal.
    def heuristic(node):
        gameState = node.gameState
        isolatedPegs = 0
        for i in range(7):
            for j in range(7):
                if i-1 >= 0 and i+1 < 7 and j-1 >= 0 and j+1 < 6:
                    if (gameState[i][j] == 1 and
                        (gameState[i][j-1] == -1 or gameState[i][j-1] == 0) and
                        (gameState[i][j+1] == -1 or gameState[i][j+1] == 0) and
                        (gameState[i-1][j] == -1 or gameState[i-1][j] == 0) and
                        (gameState[i+1][j] == -1 or gameState[i+1][j] == 0)):
                        isolatedPegs = isolatedPegs + 1
                elif i-1 < 0:
                    if (gameState[i][j] == 1 and
                        (gameState[i][j-1] == -1 or gameState[i][j-1] == 0) and
                        (gameState[i][j+1] == -1 or gameState[i][j+1] == 0) and
                        (gameState[i+1][j] == -1 or gameState[i+1][j] == 0)):
                        isolatedPegs = isolatedPegs + 1
                elif i+1 >= 7:
                    if (gameState[i][j] == 1 and
                        (gameState[i][j-1] == -1 or gameState[i][j-1] == 0) and
                        (gameState[i][j+1] == -1 or gameState[i][j+1] == 0) and
                        (gameState[i-1][j] == -1 or gameState[i-1][j] == 0)):
                        isolatedPegs = isolatedPegs + 1
                elif j-1 < 0:
                    if (gameState[i][j] == 1 and
                        (gameState[i][j+1] == -1 or gameState[i][j+1] == 0) and
                        (gameState[i-1][j] == -1 or gameState[i-1][j] == 0) and
                        (gameState[i+1][j] == -1 or gameState[i+1][j] == 0)):
                        isolatedPegs = isolatedPegs + 1
                elif j+1 >=7:
                    if (gameState[i][j] == 1 and
                        (gameState[i][j-1] == -1 or gameState[i][j-1] == 0) and
                        (gameState[i-1][j] == -1 or gameState[i-1][j] == 0) and
                        (gameState[i+1][j] == -1 or gameState[i+1][j] == 0)):
                        isolatedPegs = isolatedPegs + 1
        return isolatedPegs-1
    
    def bfs(parent):
        PQueue.put((heuristic(parent),parent))
        while not PQueue.empty():
            node = PQueue.get()[1]
            if GoalTest(node.gameState):
                # Once goal found the trace is the current nodes trace:
                pegSolitaireObject.trace = node.trace
                return 1
            for child in children(node,pegSolitaireObject):
                childState = [tuple(i) for i in child.gameState]
                childState = tuple(childState)
                if childState not in visitedStates:
                    visitedStates.add(childState)
                    pegSolitaireObject.nodesExpanded += 1
                    newPos = pegSolitaireObject.trace.pop()
                    oldPos = pegSolitaireObject.trace.pop()
                    child.trace.append(oldPos)
                    child.trace.append(newPos)
                    PQueue.put((heuristic(child),child))
                else:
                    pegSolitaireObject.trace.pop()
                    pegSolitaireObject.trace.pop()
                
        return
    
    visitedStates = set()
    if bfs(pegSolitaireObject) is None:
        print "Solution Not Found"
    return
