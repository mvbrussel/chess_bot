import numpy as np
import pygame
import random
import chess

# from globals import square_size, white_move, board, selected_piece, selected_square
from utils import globals


class HumanPlayer:
    
    def __init__(self, colour):
        self.colour = colour 
        self.selected_piece = None

    def move(self, board, event):
        
       
        #Get the corresponding square
        square = self.coordinates_to_square(coords=pygame.mouse.get_pos())
        
        #Convert the string representation to a square
        parsed_square = chess.parse_square(square)
        
        #Find the piece at the square
        piece = board.piece_at(parsed_square)

        
        #When an empty square is clicked
        if piece is None: 
            
            print('empty square clicked')
            
            if globals.selected_square is not None:
            
                #Check if valid move
                proposed_move_uci = globals.selected_square + square
                proposed_move = chess.Move.from_uci(proposed_move_uci)
                
                if proposed_move in board.legal_moves:
                    board.push(proposed_move)
                    globals.white_move = False
                    globals.selected_piece = None
                    globals.selected_square = None
            
        #When a black piece is clicked
        elif piece.symbol().islower() is True and globals.selected_square is not None:
        # elif piece.color == chess.BLACK and globals.selected_square is not None:
            
            print('black piece clicked')
            
            #Check if valid move
            proposed_move_uci = globals.selected_square + square
            proposed_move = chess.Move.from_uci(proposed_move_uci)
            
            if proposed_move in board.legal_moves:
                board.push(proposed_move)
                globals.white_move = False
                globals.selected_piece = None
                globals.selected_square = None
        
        #Select a new piece if a white piece is clicked
        elif piece.symbol().isupper() is True:
        # elif piece.color == chess.WHITE:
            
            print('white piece clicked')
            
            globals.selected_piece = piece
            globals.selected_square = square
         
             
        return
    
    @staticmethod
    def coordinates_to_square(coords):
        
        # Finding coordinates and converting to letter
        letter = ord('a') + coords[0] // globals.square_size
        number = coords[1] // globals.square_size + 1

        #Check if needed
        # if human_white:
        #     number = 9 - number   
        
        number = 9 - number     

        letter = chr(letter)

        return '{}{}'.format(letter, number)

class AIPlayer:
    def __init__(self):
        pass

    def input_move(self, board):
        
        valid_proposed_move = False
        
        while valid_proposed_move is False:
            
            proposed_move_uci = input("Please enter a chess move in uci format: ")
            
            proposed_move = chess.Move.from_uci(proposed_move_uci)
            
            if proposed_move in board.legal_moves:
                board.push(proposed_move)
                globals.white_move = True
                valid_proposed_move = True
                
    
                
            
                
            
        

        
