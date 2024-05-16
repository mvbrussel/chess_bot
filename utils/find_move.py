#Import modules
import chess
import numpy as np

#Defining the functiong for finding moves
def find_move(fen1, fen2):
    # Create board objects from FEN positions
    # fen1 = x['fen']
    # fen2 = x['next_fen']
    
    board1 = chess.Board(fen1)
    board2 = chess.Board(fen2)

    # Find the move made between the two positions
    move = np.nan
    for possible_move in board1.legal_moves:
        # Make the move on a copy of the first board
        temp_board = board1.copy()
        temp_board.push(possible_move)
        
        # Compare the resulting FEN position with the second position
        if temp_board==board2:
            move = possible_move
            move = move.uci()
            break

    return move
