# Loading modules
import pygame
import numpy as np
from utils import globals

#! Define in different file
board_colour = (107, 142, 35)
square_size = 75
FROM_COLOUR = (187, 203, 61)
TO_COLOUR = (246, 246, 127)

# Loading the chess pieces images
wp = pygame.image.load("chess_game/images/white_pawn.gif")
bp = pygame.image.load("chess_game/images/black_pawn.gif")
wn = pygame.image.load("chess_game/images/white_knight.gif")
bn = pygame.image.load("chess_game/images/black_knight.gif")
wb = pygame.image.load("chess_game/images/white_bishop.gif")
bb = pygame.image.load("chess_game/images/black_bishop.gif")
wr = pygame.image.load("chess_game/images/white_rook.gif")
br = pygame.image.load("chess_game/images/black_rook.gif")
wq = pygame.image.load("chess_game/images/white_queen.gif")
bq = pygame.image.load("chess_game/images/black_queen.gif")
wk = pygame.image.load("chess_game/images/white_king.gif")
bk = pygame.image.load("chess_game/images/black_king.gif")
switch = pygame.image.load("chess_game/images/switch.png")
switch = pygame.transform.scale(switch, (50, 60))
restart = pygame.image.load("chess_game/images/restart.png")
restart = pygame.transform.scale(restart, (40, 40))

# When running in interactive window
# wp = pygame.image.load('chess_gui/images/white_pawn.gif')
# bp = pygame.image.load('chess_gui/images/black_pawn.gif')
# wn = pygame.image.load('chess_gui/images/white_knight.gif')
# bn = pygame.image.load('chess_gui/images/black_knight.gif')
# wb = pygame.image.load('chess_gui/images/white_bishop.gif')
# bb = pygame.image.load('chess_gui/images/black_bishop.gif')
# wr = pygame.image.load('chess_gui/images/white_rook.gif')
# br = pygame.image.load('chess_gui/images/black_rook.gif')
# wq = pygame.image.load('chess_gui/images/white_queen.gif')
# bq = pygame.image.load('chess_gui/images/black_queen.gif')
# wk = pygame.image.load('chess_gui/images/white_king.gif')
# bk = pygame.image.load('chess_gui/images/black_king.gif')
# switch = pygame.image.load('chess_gui/images/switch.png')
# switch = pygame.transform.scale(switch, (50, 60))
# restart = pygame.image.load('chess_gui/images/restart.png')
# restart = pygame.transform.scale(restart, (40, 40))


def pixel_to_square_index(pixel_coords):
    """Convert pixel coordinates to square indices"""

    x = pixel_coords[0] // square_size
    y = pixel_coords[1] // square_size

    return x, y


def draw_background(win):
    """Draw the chess board and color the squares of the moved/selected piece"""

    win.fill((255, 255, 255))

    for x in range(8):
        for y in range(0, 8):
            if (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
                pygame.draw.rect(
                    win,
                    board_colour,
                    (x * square_size, y * square_size, square_size, square_size),
                )

    if globals.from_square:
        from_x, from_y = pixel_to_square_index(globals.from_square)
        pygame.draw.rect(
            win,
            FROM_COLOUR,
            (from_x * square_size, from_y * square_size, square_size, square_size),
        )

    if globals.to_square:
        to_x, to_y = pixel_to_square_index(globals.to_square)
        pygame.draw.rect(
            win,
            FROM_COLOUR,
            (to_x * square_size, to_y * square_size, square_size, square_size),
        )

    win.blit(switch, (625, 200))
    win.blit(restart, (630, 320))


def fen_to_array(fen):
    """
    Convert a FEN (Forsyth–Edwards Notation) string representing a chess position
    to a 2D array representation.

    Args:
        fen (str): The FEN string representing the chess position.

    Returns:
        list: A 2D list representing the chess position, where each element
        represents a square on the chessboard. Empty squares are represented
        by '.' and pieces are represented by their corresponding FEN symbols.
    """

    fen = fen.split()[0]

    arr = []

    rows = fen.split("/")
    for row in rows:
        row_arr = []
        for ch in str(row):
            if ch.isdigit():
                for _ in range(int(ch)):
                    row_arr.append(".")
            else:
                row_arr.append(ch)
        arr.append(row_arr)

    return arr


def draw_pieces(win, fen):
    """Draw the chess pieces on the generated board, given the FEN position"""

    arr = fen_to_array(fen=fen)

    piece_to_variable = {
        "p": bp,
        "n": bn,
        "b": bb,
        "r": br,
        "q": bq,
        "k": bk,
        "P": wp,
        "N": wn,
        "B": wb,
        "R": wr,
        "Q": wq,
        "K": wk,
    }

    for x in range(8):
        for y in range(8):
            if arr[y][x] == ".":
                continue
            piece = piece_to_variable[arr[y][x]]
            win.blit(piece, (x * square_size, y * square_size))
