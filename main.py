# Importing modules
import pygame
import chess
from keras.models import load_model

# Importing local modules
from chess_game.human_player import HumanPlayer
from chess_game.ai_player import AIPlayer
from chess_game.stockfish_player import StockfishPlayer
from chess_game.draw_board import draw_background, draw_pieces
from utils import globals
from utils.reset_game import reset

# Set whether the stockfish engine or human player is used
human_player = False
stockfish_skill = 20

# Initialize the variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
run = True
globals.white_move = True
globals.board = chess.Board()
black = AIPlayer()

if human_player is True:
    white = HumanPlayer(colour="white")
elif human_player is False:
    white = StockfishPlayer(skill_level=stockfish_skill)

# Initialize the game
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
fps_clock = pygame.time.Clock()

# Load the model
model = load_model("move_prediction/saved_models/initial_model.h5")

# Start the game
while run:
    fps_clock.tick(30)
    draw_background(win=win)
    draw_pieces(win=win, fen=globals.board.fen())
    pygame.display.update()

    # When it is White's turn and a human is playing
    if globals.white_move is True and human_player is True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 630 <= x <= 670 and 320 <= y <= 360:  # Reset
                    reset()

                else:
                    white.move(board=globals.board, event=event)

                    if globals.board.is_checkmate():
                        print("White won")
                        reset()
                        run = False

    # When it is White's turn and the Stockfish engine is playing
    elif globals.white_move is True and human_player is False:
        white.move(board=globals.board)

        if globals.board.is_checkmate():
            print("White won")
            reset()
            run = False

    # When it is Black's turn
    elif globals.white_move is False:
        predictions = black.predict_move(board=globals.board, model=model)
        black.move(board=globals.board, predictions=predictions)

        if globals.board.is_checkmate():
            print("Black won")
            reset()
            run = False
