from utils import globals

def reset():
    """Function for resetting the game whilst playing"""    
    globals.board.reset()
    globals.white_move = True 
    globals.from_square = None 
    globals.to_square = None
    globals.selected_square = None
    globals.selected_piece = None