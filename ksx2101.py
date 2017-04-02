from __future__ import absolute_import
from engines import Engine
from copy import deepcopy
import random

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        #count of the number of generated nodes
        self.node_count = 0 
        #for calculating average branching factor
        self.branches = []
        #for keeping track of duplicate nodes
        self.dictionary = {}
        #2D array assignment every board position a weighted value
        self.square_weights = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]


    #Converts a board to an equivalent string representation.
    #Used for the dictionary that keeps track of duplicate nodes.
    def board_to_string(self, board):
        #Final string to be returned
        final_str = ''
        for y in range(7,-1,-1):
            for x in range(8):
                # Get the piece to print
                piece = board[x][y]
                if piece == -1: 
                    final_str = final_str + 'B'
                elif piece == 1: 
                    final_str = final_str + 'W'
                else:
                    final_str = final_str + '.'

        return final_str


    #Evalutes the weighted score of the board for a color
    def evaluate(self, board, color):
        opponent = -color
        total = 0

        #Get a list of your squares
        my_squares = board.get_squares(color)
        #Evaluate the weighted score of each square and add it to the total
        for square in my_squares:
            total += self.square_weights[square[0]][square[1]]

        #Get a list of your opponent's squares
        opp_squares = board.get_squares(opponent)
        #Evaluate the weighted score of each square and subtract it from the total
        for square in opp_squares:
            total -= self.square_weights[square[0]][square[1]]

        #Return the total weighted score    
        return total


    #Recursive minimax function, based on lecture slides
    def do_minimax(self, board, color, depth):
        #This was for the statistics section. Commented it out now
        #self.node_count += 1

        if depth == 0:
            return (self.evaluate(board, color), None)

        move_list = board.get_legal_moves(color)
        
        #This was for the statistics section. Commented it out now
        #self.branches.append(len(move_list))

        if not move_list:
            return (self.evaluate(board, color), None)
        
        best_score = -100000
        best_move = None

        for move in move_list:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)

            """
            For keeping track of duplicate nodes in the statistics section.
            Commented it out now.

            board_string = self.board_to_string(new_board)
            if board_string in self.dictionary:
                self.dictionary[board_string] = self.dictionary[board_string] + 1
            else:
                self.dictionary[board_string] = 1
            """

            try_tuple = self.do_minimax(new_board, -color, depth-1)
            try_score = -try_tuple[0]

            if try_score > best_score:
                best_score = try_score
                best_move = move

        return (best_score, best_move)


    #Minimax with alpha-beta, based on lecture slides
    def do_minimax_with_alpha_beta(self, board, color, depth, my_best, opp_best):
        #This was for the statistics section. Commented it out now
        #self.node_count += 1

        if depth == 0:
            return (self.evaluate(board, color), None)

        move_list = board.get_legal_moves(color)
        
        #This was for the statistics section. Commented it out now
        #self.branches.append(len(move_list))

        if not move_list:
            return (self.evaluate(board, color), None)

        best_score = my_best
        best_move = None

        for move in move_list:
            new_board = deepcopy(board)
            new_board.execute_move(move, color)

            """
            For keeping track of duplicate nodes in the statistics section.
            Commented out now.

            board_string = self.board_to_string(new_board)
            if board_string in self.dictionary:
                self.dictionary[board_string] = self.dictionary[board_string] + 1
            else:
                self.dictionary[board_string] = 1
            """

            try_tuple = self.do_minimax_with_alpha_beta(new_board, -color, depth-1, -opp_best, -best_score)
            try_score = -try_tuple[0]

            if try_score > best_score:
                best_score = try_score
                best_move = move

            if best_score > opp_best:
                return (best_score, best_move)

        return (best_score, best_move)


    def get_move(self, board, color, move_num=None, time_remaining=None, time_opponent=None):

        #print 'Time remaining:', time_remaining

        #No alpha-beta pruning
        if (self.alpha_beta == False):

            #If there's more than 12 seconds left, use ply 4
            if (time_remaining > 12.0):
                return self.do_minimax(board, color, 4)[1]

            #If there's more than 1 seconds left, use ply 3
            elif (time_remaining > 1.0):
                return self.do_minimax(board, color, 3)[1]

            #Otherwise, pick a random move
            else:
                move_list = board.get_legal_moves(color)
                return random.choice(move_list)

        #With alpha-beta pruning
        else:
            #If there's more than 12 seconds left, use ply 4
            if (time_remaining > 12.0):
                return self.do_minimax_with_alpha_beta(board, color, 4, -100000, 100000)[1]

            #If there's more than 1 seconds left, use ply 3    
            elif (time_remaining > 1.0):
                return self.do_minimax_with_alpha_beta(board, color, 3, -100000, 100000)[1]

            #Otherwise, pick a random move
            else:
                move_list = board.get_legal_moves(color)
                return random.choice(move_list)

    """    
    #This was used for determining statistics in Part II
    def __del__(self):

        #Print the node count
        print 'Node count: ', self.node_count

        #Calculate the average branching factor and print it out
        if len(self.branches) != 0:
            average = (1.0 * sum(self.branches)) / len(self.branches)
            print 'Average branching factor: ', average

        #Find the number of duplicated nodes and print it out
        duplicate_count = 0 
        for count in self.dictionary.values():
            if count > 1:
                duplicate_count += 1

        print 'Duplicate count: ', duplicate_count
    """           

    #Left over from skeleton code
    def _get_cost(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op
        
engine = StudentEngine


