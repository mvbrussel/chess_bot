import chess
import numpy as np


def encode_move(move_uci):
    # Convert move to uci format
    # Encode move in a vector representation
    move_encoded = np.zeros((64, 64), dtype=np.int8)
    move_encoded[move_uci.from_square][move_uci.to_square] = 1
    
    move_encoded_flat = move_encoded.flatten()
    move_index = np.argmax(move_encoded_flat)
    
    return move_index


def decode_move(move_index):
    # Convert the single integer representation back into 2D array indices
    row_index, col_index = divmod(move_index, 64)
    
    # Convert the row and column indices into square notation in UCI format
    from_square = chess.square_name(row_index)
    to_square = chess.square_name(col_index)
    uci_string = from_square + to_square
    
    # Return the UCI move
    return chess.Move.from_uci(uci_string)


def find_move(fen1, fen2):
    # Create board objects from FEN positions
    # fen1 = x['fen']
    # fen2 = x['next_fen']
    
    board1 = chess.Board(fen1)
    board2 = chess.Board(fen2)

    # Find the move made between the two positions
    move = None
    for possible_move in board1.legal_moves:
        # Make the move on a copy of the first board
        temp_board = board1.copy()
        temp_board.push(possible_move)
        
        # Compare the resulting FEN position with the second position
        if temp_board==board2:
            move = possible_move
            break

    return move