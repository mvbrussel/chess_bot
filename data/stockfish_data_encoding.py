# For running in interactive terminal
import sys
projec_dir = "c:\\Users\\Marieke\\GitHub\\chess_bot"
sys.path.append(projec_dir)

import chess
import numpy as np
import os

from utils.move_encoding import encode_move
from utils.board_encoding import encode_board_from_fen

#function to encode all moves and positions from rawData folder
def encodeAllMovesAndPositions():
    
    board = chess.Board() #this is used to change whose turn it is so that the encoding works
    board.turn = False #set turn to black first, changed on first run

    #find all files in folder:
    files = os.listdir('stockfish_generated_data/raw_data')
    for idx, f in enumerate(files):
        print(idx)
        movesAndPositions = np.load(f'stockfish_generated_data/raw_data/{f}', allow_pickle=True)
        moves = movesAndPositions[:,0]
        positions = movesAndPositions[:,1]
        encodedMoves = []
        encodedPositions = []

        for i in range(len(moves)):
            board.turn = (not board.turn) #swap turns
            try:
                encodedMoves.append(encode_move(moves[i], board)) 
                encodedPositions.append(encode_board_from_fen(positions[i]))
            except:
                try:
                    board.turn = (not board.turn) #change turn, since you  skip moves sometimes, you  might need to change turn
                    encodedMoves.append(encode_move(moves[i], board)) 
                    encodedPositions.append(encode_board_from_fen(positions[i]))
                except:
                    print(f'error in file: {f}')
                    print("Turn: ", board.turn)
                    print(moves[i])
                    print(positions[i])
                    print(i)
                    break
            
        np.save(f'stockfish_generated_data/prepared_data/moves{idx}', np.array(encodedMoves))
        np.save(f'stockfish_generated_data/prepared_data/positions{idx}', np.array(encodedPositions))
    
encodeAllMovesAndPositions()

#NOTE: shape of files:
#moves: (number of moves in gamew)
#positions: (number of moves in game, 8, 8, 14) (number of moves in game is including both black and white moves)

#dataset

