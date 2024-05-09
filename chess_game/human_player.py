# Import modules
import numpy as np
import pygame
import random
import chess

# Import local modules
from utils import globals

class HumanPlayer:
    def __init__(self, colour):
        self.colour = colour
        self.selected_piece = None

    def move(self, board, event):
        """
        Defines the logic for making moves with White when a square is clicked in the game
        """

        # Get the corresponding square
        coords = pygame.mouse.get_pos()
        square = self.coordinates_to_square(coords=coords)

        # Convert the string representation to a square
        parsed_square = chess.parse_square(square)

        # Find the piece at the square
        piece = board.piece_at(parsed_square)

        # When a white piece is selected and an empty square is clicked
        if piece is None and globals.selected_square is not None:
            # Check if valid move
            proposed_move_uci = globals.selected_square + square
            proposed_move = chess.Move.from_uci(proposed_move_uci)

            # Make move if it is valid
            if proposed_move in board.legal_moves:
                board.push(proposed_move)
                globals.white_move = False
                globals.selected_piece = None
                globals.selected_square = None
                globals.to_square = coords

        # When a white piece is selected and a black piece is clicked
        elif piece.symbol().islower() is True and globals.selected_square is not None:
            # Check if valid move
            proposed_move_uci = globals.selected_square + square
            proposed_move = chess.Move.from_uci(proposed_move_uci)

            # Make the move if valid
            if proposed_move in board.legal_moves:
                board.push(proposed_move)
                globals.white_move = False
                globals.selected_piece = None
                globals.selected_square = None
                globals.to_square = coords

        # Select a new piece if a white piece is clicked
        elif piece.symbol().isupper() is True:
            globals.selected_piece = piece
            globals.selected_square = square
            globals.from_square = coords
            globals.to_square = None

        return

    @staticmethod
    def coordinates_to_square(coords):
        """Convert coordinates on a Pygame window to a chess square notation (e.g., 'a1', 'e5', etc.)"""

        # Finding coordinates and converting to letter
        letter = ord("a") + coords[0] // globals.square_size
        number = coords[1] // globals.square_size + 1
        number = 9 - number
        letter = chr(letter)

        return "{}{}".format(letter, number)
