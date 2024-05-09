# Loading modules
from keras.models import load_model
import chess
import numpy as np
import os
import pandas as pd
import sys

# Loading local modules
project_dir = "c:\\Users\\Marieke\\GitHub\\chess_bot"
sys.path.append(project_dir)
from utils.board_encoding import encode_board, fen_to_board
from utils.move_encoding import encode_move, decode_move
from utils import globals

# For running in the interactive terminal
# cwd = os.getcwd()
# model_path = os.path.join(cwd, "../move_prediction/saved_models/testing_model.h5")
# model = load_model(model_path)


#! Functions: add variable types, add overall description according to best practices
#! Move to draw board file
def algebraic_to_pixel_coords(algebraic_notation):
    # Convert algebraic notation to square indices
    column_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column = column_map[algebraic_notation[0]]
    row = int(algebraic_notation[1]) - 1

    # Calculate pixel coordinates of the center of the square
    # Flip the y-coordinate because the origin is at the top-left
    x = (column + 0.5) * 75
    y = (7 - row + 0.5) * 75
    return x, y


class AIPlayer:
    def __init__(self):
        pass

    def predict_move(self, board, model):
        """
        Predict the optimal move given a board position and trained model

        Args:
            board (chess.Board): the current board position
            model: trained model

        Returns:
            dataframe with the variables:
                all possible encoded moves
                corresponding decoded moves
                predicted probability of each move
        """

        # Reshape to input for predictions
        encoded_board = encode_board(board)
        encoded_board = encoded_board.reshape(1, 896)

        # Obtain the predictions
        prediction = (
            model(encoded_board)
            .numpy()
            .reshape(
                4672,
            )
        )
        df_prediction = pd.DataFrame(prediction, columns=["probability"])
        #! Check if this is correct
        df_prediction["encoded_move"] = df_prediction.index + 1

        # Adding the decoded moves
        df_prediction["decoded_move"] = ""
        for i in range(len(df_prediction)):
            try:
                df_prediction.loc[i, "decoded_move"] = decode_move(
                    df_prediction.loc[i, "encoded_move"], board
                )
            except:
                pass

        return df_prediction

    def move(self, board, predictions):
        """
        Determine the optimal move to make given the model predictions, and make the move on the globally defined board variable

        Args:
            board (chess.Board): the current board position
            predictions (dataframe): dataframe with the predicted probability of all possible moves
                all possible encoded moves
                corresponding decoded moves
                predicted probability of each move

        """

        # Find all valid moves
        legal_moves = list(board.legal_moves)

        # Filter the predictions to find only the legal moves and sort on probability
        legal_predictions = predictions[predictions["decoded_move"].isin(legal_moves)]
        legal_predictions = legal_predictions.sort_values(
            by="probability", ascending=False
        ).reset_index(drop=True)

        # Find and make the optimal move
        max_idx = legal_predictions["probability"].idxmax()
        predicted_move = legal_predictions.loc[max_idx, "decoded_move"]
        board.push(predicted_move)

        # Update global variables
        globals.white_move = True
        # For coloring the board
        #! Move parts to draw_board file
        from_square_uci = chess.square_name(predicted_move.from_square)
        to_square_uci = chess.square_name(predicted_move.to_square)
        globals.from_square = algebraic_to_pixel_coords(from_square_uci)
        globals.to_square = algebraic_to_pixel_coords(to_square_uci)

        pass
