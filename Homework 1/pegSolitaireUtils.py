import config
import readGame

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
    
    _CORNER_INDICES = [0, 1, 5, 6]
    
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.trace = []    
    
    def is_corner(self, pos):
        ########################################
        # You have to make changes from here
        # check for if the new positon is a corner or not
        # return true if the position is a corner
        return pos[0] in game._CORNER_INDICES and pos[1] in game._CORNER_INDICES
    
    def getNextPosition(self, oldPos, direction):
        #########################################
        # YOU HAVE TO MAKE CHANGES HERE
        # See DIRECTION dictionary in config.py and add
        # this to oldPos to get new position of the peg if moved
        # in given direction , you can remove next line
        
        # Returning position after moving by 1 step in the given direction:
        return (oldPos[0] + config.DIRECTION[direction][0],
                oldPos[1] + config.DIRECTION[direction][1])
    
    def is_validMove(self, oldPos, direction):
        #########################################
        # DONT change Things in here
        # In this we have got the next peg position and
        # below lines check for if the new move is a corner
        adjacentPos = self.getNextPosition(oldPos, direction) # neighbour of oldPos
        newPos = self.getNextPosition(adjacentPos, direction)
        if self.is_corner(newPos):
            return False    
        #########################################
        
        ########################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # check for cases like:
        # if new move is already occupied
        # or new move is outside peg Board
        # Remove next line according to your convenience
        
        # Check if newPos is out of the board:
        if newPos[0] > 6 or newPos[1] > 6 or newPos[0] < 0 or newPos[1] < 0:
            return False
        # Check whether oldPos holds peg:
        if self.gameState[oldPos[0]][oldPos[1]] != 1:
            return False
        # Check whether adjacentPos holds a peg:
        if self.gameState[adjacentPos[0]][adjacentPos[1]] != 1:
            return False
        # Check whether newPos is available:
        if self.gameState[newPos[0]][newPos[1]] != 0:
            return False
        
        return True
    
    def getNextState(self, oldPos, direction):
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            print "Error, You are not checking for valid move"
            exit(0)
        ###############################################
        
        ###############################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # Update the gameState after moving peg
        # eg: remove crossed over pegs by replacing it's
        # position in gameState by 0
        # and updating new peg position as 1
        adjacentPos = self.getNextPosition(oldPos, direction)
        newPos = self.getNextPosition(adjacentPos, direction)
        self.gameState[oldPos[0]][oldPos[1]] = 0
        self.gameState[adjacentPos[0]][adjacentPos[1]] = 0
        self.gameState[newPos[0]][newPos[1]] = 1
        return    
