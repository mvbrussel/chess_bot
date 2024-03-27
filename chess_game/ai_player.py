#To enable importing in the interactive window
import sys
project_dir = 'c:\\Users\\Marieke\\GitHub\\chess_bot'
sys.path.append(project_dir)

from keras.models import load_model
from utils import globals
import chess
from utils.board_encoding import encode_board, fen_to_board
import numpy as np
import os
import pandas as pd

#For running in the interactive terminal
cwd = os.getcwd()
model_path = os.path.join(cwd, "../move_prediction/saved_models/testing_model.h5")
model = load_model(model_path)




class AIPlayer:
    
    def __init__():
        pass
    
    def predict_move(board, model):
        
        encoded_board = encode_board(board)
        
        #Reshape to input for predictions
        encoded_board = encoded_board.reshape(1,896)
        prediction = model(encoded_board).numpy().reshape(4672,)
        df_prediction = pd.DataFrame(prediction, columns=['probability'])
        df_prediction['encoded_move'] = df_prediction.index + 1
        
        #! Add line for adding the move that corresponds with the encoded value 
        
        return df_prediction
    
    def move(board, predictions):
        
        encoded_board = encode_board(board)
        
        #Reshape to input for predictions
        encoded_board = encoded_board.reshape(1,896)
        
        #Make predictions and reshape into an array
        
        
        
        
        
        pass
        
        
 
