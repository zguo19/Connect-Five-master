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
        AIPlayer.__init__(self, "A20368154", "x", 4)
        

    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

        
    def abPrunning(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """
        
        # enumerate all legal moves from this state
        def legalMoves(state):
            legal_moves = []
            for i in range(options.getCols()):
                # if column i is a legal move...
                if self.isLegalMove(i, state):
                    # make the move in column i for curr_player
                    temp = self.makeMove(state, i, curr_player)
                    legal_moves.append(temp)
            return legal_moves

        def abmax(state, depth, alpha, beta): #for current player, color[0], so value(state, self.colors[o])
            v = -99999999
            for col in range(options.getCols()):
                if self.isLegalMove(col, state):
                    v = max(v, abmin(state, depth-1, alpha, beta))
                if v >= beta:
                    return v   
                alpha=max(alpha, v)
            return v

        def abmin(state, depth, alpha, beta):
            v = +99999999
            for col in range(options.getCols()):
                if self.isLegalMove(col, state):
                    v = min(v, abmax(state, depth-1, alpha, beta))
                if v <= alpha:
                    return v   
                beta=min(beta, v)
            return v
        
        legal_moves = legalMoves(state)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        values = []
        v = None

        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            v = max(v, -self.abmin(child, depth-1, -99999999, +99999999))
            values.append(v)
        largest=max(values)
        best_move = values.index(largest)

        return best_move, largest

        



    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        
        # sleeping for about 1 second makes it looks like he's thinking
        #time.sleep(random.randrange(8, 17, 1)/10.0)
        #return random.randint(0, 6)
            
        m = Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        print(value)
        return best_move