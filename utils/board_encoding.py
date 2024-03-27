import numpy as np
import chess

def fen_to_board(fen: str):
 board = chess.Board(fen)
 return board


def encode_board(board: chess.Board) -> np.array:
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
