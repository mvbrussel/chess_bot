#To enable importing in the interactive window
import sys
project_dir = 'c:\\Users\\Marieke\\GitHub\\chess_bot'
sys.path.append(project_dir)

from keras.models import load_model
from utils import globals
import chess
from utils.board_encoding import encode_board, fen_to_board
from utils.move_encoding import encode_move, decode_move
import numpy as np
import os
import pandas as pd

#For running in the interactive terminal
# cwd = os.getcwd()
# model_path = os.path.join(cwd, "../move_prediction/saved_models/testing_model.h5")
# model = load_model(model_path)




class AIPlayer:

    
    def predict_move(self, board, model):        
        
        # print(board)
        
        encoded_board = encode_board(board)
        #Reshape to input for predictions
        encoded_board = encoded_board.reshape(1,896)
        prediction = model(encoded_board).numpy().reshape(4672,)
        df_prediction = pd.DataFrame(prediction, columns=['probability'])
        df_prediction['encoded_move'] = df_prediction.index + 1
        
        #Adding the decoded moves
        df_prediction['decoded_move'] = ""
        for i in range(len(df_prediction)):
            
            try: 
                df_prediction.loc[i, 'decoded_move'] = decode_move(df_prediction.loc[i, 'encoded_move'], board)
            except:
                pass
        
        return df_prediction
    
    def move(self, board, predictions):
        
        #Find all valid moves
        legal_moves = list(board.legal_moves)     
        
        #Filter the predictions to find only the legal mvoes
        legal_predictions = predictions[predictions['decoded_move'].isin(legal_moves)]
        legal_predictions = legal_predictions.sort_values(by='probability', ascending=False).reset_index(drop=True)
        
        #For printing
        # print(legal_predictions.head(10))
        predictions = predictions.sort_values(by='probability', ascending=False).reset_index(drop=True)
        print(predictions.head(10))
        
        
        #Continued code
        max_idx = legal_predictions['probability'].idxmax()
        predicted_move = legal_predictions.loc[max_idx, 'decoded_move']
        
        board.push(predicted_move)
        globals.white_move = True      
        
        
        pass
        
        
 
