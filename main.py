import pygame 
import chess 

from chess_game.human_player import HumanPlayer
from chess_game.ai_player import AIPlayer
from chess_game.draw_board import draw_background, draw_pieces
from utils import globals
from keras.models import load_model

#Initialize the variables
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

run = True 
globals.white_move = True
globals.board = chess.Board()
white = HumanPlayer(colour='white')
black = AIPlayer()

#Initialize the game
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess')
fps_clock = pygame.time.Clock()

#Load the model
model = load_model("move_prediction/saved_models/testing_model.h5")

def reset():
    globals.board.reset()
    globals.white_move = True 
    globals.from_square = None 
    globals.to_square = None

while run:
    
    fps_clock.tick(30)
    draw_background(win=win)
    draw_pieces(win=win, fen=globals.board.fen())
    pygame.display.update()
    

    if globals.white_move is True:
        
        events = pygame.event.get()

        for event in events:
            
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()                

                if 630 <= x <= 670 and 320 <= y <= 360: # Reset
                    reset()
                    
                else:
                    print('white making move')
                    print('The event: ' + str(event))

                    white.move(board=globals.board, event=event)
                    
                    if globals.board.is_checkmate():
                        reset()
            

                
    elif globals.white_move is False:
        
        print(globals.board)
        print(model)
        predictions = black.predict_move(board=globals.board, model=model)
        black.move(board=globals.board, predictions=predictions)
        
        if globals.board.is_checkmate():
            reset()
            
            
