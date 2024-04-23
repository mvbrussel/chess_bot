#For running in interactive terminal
import sys
projec_dir = 'c:\\Users\\Marieke\\GitHub\\chess_bot'
sys.path.append(projec_dir)

#Adding stockfish to the path
stockfish_dir = 'c:\\Users\\Marieke\\GitHub\\chess_bot\\stockfish'
sys.path.append(stockfish_dir)

from stockfish import Stockfish
import chess
from utils import globals

class StockfishPlayer:
    
    def __init__(self, skill_level):
        self.engine = Stockfish(path='c:\\Users\\Marieke\\GitHub\\chess_bot\\stockfish\stockfish')
        self.engine.set_skill_level(skill_level)
        self.colour = None

    def move(self, board):
        
        fen = board.fen()
        self.engine.set_fen_position(fen)
        move = self.engine.get_best_move()
        board.push_uci(move)
        globals.white_move = False
        
        pass