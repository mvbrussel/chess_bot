# For running in interactive terminal
import sys
projec_dir = "c:\\Users\\Marieke\\GitHub\\chess_bot"
sys.path.append(projec_dir)

# Loading modules

from stockfish import Stockfish
import chess
import random
from pprint import pprint
import numpy as np
import os
import glob
import time

# Adding stockfish to the path
stockfish_dir = "c:\\Users\\Marieke\\GitHub\\chess_bot\\stockfish"
sys.path.append(stockfish_dir)

stockfish = Stockfish(
            path="c:\\Users\\Marieke\\GitHub\\chess_bot\\stockfish\stockfish"
        )

#helper functions:
def checkEndCondition(board):
 if (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves() or board.can_claim_draw()):
  return True
 return False


#save
def findNextIdx():
    
 files = (glob.glob(r"C:\Users\Marieke\GitHub\chess_bot\data\stockfish_generated_data\raw_data\*.npy"))
 
 if (len(files) == 0):
  return 1 #if no files, return 1
 
 highestIdx = 0
 
 for f in files:
  file = f
  currIdx = file.split("movesAndPositions")[-1].split(".npy")[0]
  highestIdx = max(highestIdx, int(currIdx))

 return int(highestIdx)+1

def saveData(moves, positions):
 moves = np.array(moves).reshape(-1, 1)
 positions = np.array(positions).reshape(-1,1)
 movesAndPositions = np.concatenate((moves, positions), axis = 1)
 nextIdx = findNextIdx()
 
 np.save(f"stockfish_generated_data/raw_data/movesAndPositions{nextIdx}.npy", movesAndPositions)
 
 print("Saved successfully")

def runGame(numMoves, filename = "movesAndPositions1.npy"):
 """run a game you stored"""
 testing = np.load(f"stockfish_generated_data/raw_data/{filename}")
 moves = testing[:, 0]
 
 if (numMoves > len(moves)):
  print("Must enter a lower number of moves than maximum game length. Game length here is: ", len(moves))
  return

 testBoard = chess.Board()

 for i in range(numMoves):
  move = moves[i]
  testBoard.push_san(move)
 return testBoard

def mineGames(numGames : int):
 """mines numGames games of moves"""
 MAX_MOVES = 500 #don't continue games after this number

 for i in range(numGames):
  currentGameMoves = []
  currentGamePositions = []
  board = chess.Board()
  stockfish.set_position([])
  
  print(i)

  for i in range(MAX_MOVES):
   #randomly choose from those 3 moves
   moves = stockfish.get_top_moves(3)
   #if less than 3 moves available, choose first one, if none available, exit
   
   if (len(moves) == 0):
    print("game is over")
    break
   
   elif (len(moves) == 1):
    move = moves[0]["Move"]
   
   elif (len(moves) == 2):
    move = random.choices(moves, weights=(50, 50), k=1)[0]["Move"]
   
   else:
    move = random.choices(moves, weights=(50, 25, 25), k=1)[0]["Move"]

   currentGamePositions.append(stockfish.get_fen_position())
   board.push_san(move)
   currentGameMoves.append(move)
   stockfish.set_position(currentGameMoves)
   
   if (checkEndCondition(board)):
    print("game is over")
    break

  saveData(currentGameMoves, currentGamePositions)
  
mineGames(10000)