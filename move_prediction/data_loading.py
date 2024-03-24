import sqlite3
import pandas as pd
import gym
import gym_chess
import chess
from gym_chess.alphazero import BoardEncoding
import numpy as np
import matplotlib.pyplot as plt

def encodeBoard(board: chess.Board) -> np.array:
 """Converts a board to numpy array representation."""

 array = np.zeros((8, 8, 14), dtype=int)

 for square, piece in board.piece_map().items():
  rank, file = chess.square_rank(square), chess.square_file(square)
  piece_type, color = piece.piece_type, piece.color
 
  # The first six planes encode the pieces of the active player, 
  # the following six those of the active player's opponent. Since
  # this class always stores boards oriented towards the white player,
  # White is considered to be the active player here.
  offset = 0 if color == chess.WHITE else 6
  
  # Chess enumerates piece types beginning with one, which you have
  # to account for
  idx = piece_type - 1
 
  array[rank, file, idx + offset] = 1

 # Repetition counters
 array[:, :, 12] = board.is_repetition(2)
 array[:, :, 13] = board.is_repetition(3)

 return array

def BoardFromFen(fen: str):
 board = chess.Board(fen)
 return board

def encode_move(move):
    env = gym.make('ChessAlphaZero-v0')
    env.reset() 
    try:
        encoded = env.encode(move)  
    except:
        encoded = None
    return encoded

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

database = sqlite3.connect('data/test_data.db')
df = pd.read_sql_query("SELECT * FROM evaluations LIMIT 10000", database)

df['board'] = df['fen'].apply(BoardFromFen)
df['encoded_board'] = df['board'].apply(encodeBoard)

df['next_fen'] = df['fen'].shift(-1)
df['move'] = ""
df['encoded_move'] = ""
for i in range(len(df)-1):
    df.loc[i, 'move'] = find_move(df['fen'][i], df['next_fen'][i])
    df.loc[i, 'encoded_move'] = encode_move(df['move'][i])


df.dropna(subset=['encoded_move'],inplace=True)
df.reset_index(inplace=True, drop=True)

df.to_pickle('cleaned_data.pkl')
