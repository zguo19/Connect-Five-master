#Zheng Guo's AI player

from aiplayer import *
import random
from player import Player
from connect5 import *
from options import *


class A20368154(AIPlayer):
    """ Super Player
    """


    def __init__(self):
        AIPlayer.__init__(self, "A20368154", "x", 5)
        
        
    def abPrunning(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
    
        # enumerate all legal moves from this state
        def legalMoves(state):
            legal_moves = []
            m = Minimax(state)
            for i in range(options.getCols()):
                # if column i is a legal move...
                if m.isLegalMove(i, state):
                    # make the move in column i for curr_player
                    temp = m.makeMove(state, i, curr_player)
                    legal_moves.append(temp)
            return legal_moves

        #count the nodes that saved
        #ind = 0
        def abmax(state, depth, alpha, beta): #for current player, color[0], so value(state, self.colors[o])
            #global ind
            v = -99999999
            m = Minimax(state)
            legal_moves = legalMoves(state)
            if (depth==0):
                return m.value(state, m.colors[0])
            for child in legal_moves:
                if child == None:
                    print("child == None (search)")
                #ind = ind+1
                v = max(v, abmin(state, depth-1, alpha, beta))
                if v >= beta:
                    return v   
                alpha=max(alpha, v)
            return v

        def abmin(state, depth, alpha, beta):
            #global ind
            v = +99999999
            m = Minimax(state)
            legal_moves = legalMoves(state)
            if (depth==0):
                return m.value(state, m.colors[1])            
            for child in legal_moves:
                if child == None:
                    print("child == None (search)")
                #ind = ind+1
                v = min(v, abmax(state, depth-1, alpha, beta))
                if v <= alpha:
                    return v   
                beta=min(beta, v)
            return v

        # enumerate all legal moves
        m = Minimax(state)
        v = -99999999
        values = [] # will map legal move states to their alpha values
        for col in range(options.getCols()):
            # if column i is a legal move...
            if m.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = m.makeMove(state, col, curr_player)
                v = max(v, -abmin(temp, depth-1, -99999999, +99999999))
                values.append(v)
        best_alpha = max(values)
        best_move = values.index(best_alpha)
                
        return best_move, best_alpha



    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        
        # sleeping for about 1 second makes it looks like he's thinking
        #time.sleep(random.randrange(8, 17, 1)/10.0)
        #return random.randint(0, 6)
            
        best_move, value= self.abPrunning(self.difficulty, state, self.color)
        print(value)
        return best_move