import numpy as np
from datetime import datetime
import gym
import gym_chess
import os
import chess
from gym_chess.alphazero.move_encoding import utils
from pathlib import Path
from typing import Optional

def encodeKnight(move: chess.Move) -> Optional[int]:
    """
    Encode a knight move as an integer action.

    Args:
        move (chess.Move): The knight move to encode.

    Returns:
        int or None: The encoded action if the move is a knight move, 
        otherwise None.
    """
    _NUM_TYPES: int = 8
    _TYPE_OFFSET: int = 56
    _DIRECTIONS = utils.IndexedTuple(
        (+2, +1),
        (+1, +2),
        (-1, +2),
        (-2, +1),
        (-2, -1),
        (-1, -2),
        (+1, -2),
        (+2, -1),
    )

    from_rank, from_file, to_rank, to_file = utils.unpack(move)

    delta = (to_rank - from_rank, to_file - from_file)
    is_knight_move = delta in _DIRECTIONS
    
    if not is_knight_move:
        return None

    knight_move_type = _DIRECTIONS.index(delta)
    move_type = _TYPE_OFFSET + knight_move_type

    action = np.ravel_multi_index(
        multi_index=((from_rank, from_file, move_type)),
        dims=(8, 8, 73)
    )

    return action

def encodeQueen(move: chess.Move) -> Optional[int]:
    """
    Encode a queen move as an integer action.

    Args:
        move (chess.Move): The queen move to encode.

    Returns:
        int or None: The encoded action if the move is a queen move, 
        otherwise None.
    """
    _NUM_TYPES: int = 56 # = 8 directions * 7 squares max. distance
    _DIRECTIONS = utils.IndexedTuple(
        (+1,  0),
        (+1, +1),
        ( 0, +1),
        (-1, +1),
        (-1,  0),
        (-1, -1),
        ( 0, -1),
        (+1, -1),
    )

    from_rank, from_file, to_rank, to_file = utils.unpack(move)

    delta = (to_rank - from_rank, to_file - from_file)

    is_horizontal = delta[0] == 0
    is_vertical = delta[1] == 0
    is_diagonal = abs(delta[0]) == abs(delta[1])
    is_queen_move_promotion = move.promotion in (chess.QUEEN, None)

    is_queen_move = (
        (is_horizontal or is_vertical or is_diagonal) 
            and is_queen_move_promotion
    )

    if not is_queen_move:
        return None

    direction = tuple(np.sign(delta))
    distance = np.max(np.abs(delta))

    direction_idx = _DIRECTIONS.index(direction)
    distance_idx = distance - 1

    move_type = np.ravel_multi_index(
        multi_index=([direction_idx, distance_idx]),
        dims=(8,7)
    )

    action = np.ravel_multi_index(
        multi_index=((from_rank, from_file, move_type)),
        dims=(8, 8, 73)
    )

    return action

def encodeUnder(move: chess.Move) -> Optional[int]:
    """
    Encode an underpromotion move as an integer action.

    Args:
        move (chess.Move): The underpromotion move to encode.

    Returns:
        int or None: The encoded action if the move is an underpromotion move, 
        otherwise None.
    """
    _NUM_TYPES: int = 9 # = 3 directions * 3 piece types (see below)
    _TYPE_OFFSET: int = 64
    _DIRECTIONS = utils.IndexedTuple(
        -1,
        0,
        +1,
    )
    _PROMOTIONS = utils.IndexedTuple(
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
    )

    from_rank, from_file, to_rank, to_file = utils.unpack(move)

    is_underpromotion = (
        move.promotion in _PROMOTIONS 
        and from_rank == 6 
        and to_rank == 7
    )

    if not is_underpromotion:
        return None

    delta_file = to_file - from_file

    direction_idx = _DIRECTIONS.index(delta_file)
    promotion_idx = _PROMOTIONS.index(move.promotion)

    underpromotion_type = np.ravel_multi_index(
        multi_index=([direction_idx, promotion_idx]),
        dims=(3,3)
    )

    move_type = _TYPE_OFFSET + underpromotion_type

    action = np.ravel_multi_index(
        multi_index=((from_rank, from_file, move_type)),
        dims=(8, 8, 73)
    )

    return action

def encode_move(move: str, board) -> int:
    """
    Encode a chess move as an integer action.

    Args:
        move (str): The move in UCI (Universal Chess Interface) notation.
        board (chess.Board): The chess board object representing the current board state.

    Returns:
        int: The encoded action representing the given move.
    
    Raises:
        ValueError: If the given move is not a valid move.
    """
    move = chess.Move.from_uci(move)
    if board.turn == chess.BLACK:
        move = utils.rotate(move)

    action = encodeQueen(move)

    if action is None:
        action = encodeKnight(move)

    if action is None:
        action = encodeUnder(move)

    if action is None:
        raise ValueError(f"{move} is not a valid move")

    return action

def _decodeKnight(action: int) -> Optional[chess.Move]:
    """
    Decode an encoded knight move to a chess move.

    Args:
        action (int): The encoded action representing the knight move.

    Returns:
        chess.Move or None: The decoded knight move if the action is valid, 
        otherwise None.
    """
    _NUM_TYPES: int = 8
    _TYPE_OFFSET: int = 56
    _DIRECTIONS = utils.IndexedTuple(
        (+2, +1),
        (+1, +2),
        (-1, +2),
        (-2, +1),
        (-2, -1),
        (-1, -2),
        (+1, -2),
        (+2, -1),
    )

    from_rank, from_file, move_type = np.unravel_index(action, (8, 8, 73))

    is_knight_move = (
        _TYPE_OFFSET <= move_type
        and move_type < _TYPE_OFFSET + _NUM_TYPES
    )

    if not is_knight_move:
        return None

    knight_move_type = move_type - _TYPE_OFFSET

    delta_rank, delta_file = _DIRECTIONS[knight_move_type]

    to_rank = from_rank + delta_rank
    to_file = from_file + delta_file

    move = utils.pack(from_rank, from_file, to_rank, to_file)
    return move

def _decodeQueen(action: int) -> Optional[chess.Move]:
    """
    Decode an encoded queen move to a chess move.

    Args:
        action (int): The encoded action representing the queen move.

    Returns:
        chess.Move or None: The decoded queen move if the action is valid, 
        otherwise None.
    """
    _NUM_TYPES: int = 56 # = 8 directions * 7 squares max. distance

    _DIRECTIONS = utils.IndexedTuple(
        (+1,  0),
        (+1, +1),
        ( 0, +1),
        (-1, +1),
        (-1,  0),
        (-1, -1),
        ( 0, -1),
        (+1, -1),
    )
    from_rank, from_file, move_type = np.unravel_index(action, (8, 8, 73))
    
    is_queen_move = move_type < _NUM_TYPES

    if not is_queen_move:
        return None

    direction_idx, distance_idx = np.unravel_index(
        indices=move_type,
        shape=(8,7)
    )

    direction = _DIRECTIONS[direction_idx]
    distance = distance_idx + 1

    delta_rank = direction[0] * distance
    delta_file = direction[1] * distance

    to_rank = from_rank + delta_rank
    to_file = from_file + delta_file

    move = utils.pack(from_rank, from_file, to_rank, to_file)
    return move

def _decodeUnderPromotion(action: int) -> Optional[chess.Move]:
    """
    Decode an encoded underpromotion move to a chess move.

    Args:
        action (int): The encoded action representing the underpromotion move.

    Returns:
        chess.Move or None: The decoded underpromotion move if the action is valid, 
        otherwise None.
    """
    _NUM_TYPES: int = 9 # = 3 directions * 3 piece types (see below)

    _TYPE_OFFSET: int = 64

    _DIRECTIONS = utils.IndexedTuple(
        -1,
        0,
        +1,
    )

    _PROMOTIONS = utils.IndexedTuple(
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
    )

    from_rank, from_file, move_type = np.unravel_index(action, (8, 8, 73))

    is_underpromotion = (
        _TYPE_OFFSET <= move_type
        and move_type < _TYPE_OFFSET + _NUM_TYPES
    )

    if not is_underpromotion:
        return None

    underpromotion_type = move_type - _TYPE_OFFSET

    direction_idx, promotion_idx = np.unravel_index(
        indices=underpromotion_type,
        shape=(3,3)
    )

    direction = _DIRECTIONS[direction_idx]
    promotion = _PROMOTIONS[promotion_idx]

    to_rank = from_rank + 1
    to_file = from_file + direction

    move = utils.pack(from_rank, from_file, to_rank, to_file)
    move.promotion = promotion

    return move

def decode_move(action: int, board) -> chess.Move:
    """
    Decode an encoded action to a chess move.

    Args:
        action (int): The encoded action representing the chess move.
        board (chess.Board): The chess board object representing the current board state.

    Returns:
        chess.Move: The decoded chess move.

    Raises:
        ValueError: If the given action is not a valid action.
    """
    move = _decodeQueen(action)
    is_queen_move = move is not None

    if not move:
        move = _decodeKnight(action)

    if not move:
        move = _decodeUnderPromotion(action)

    if not move:
        raise ValueError(f"{action} is not a valid action")

    # Actions encode moves from the perspective of the current player. If
    # this is the black player, the move must be reoriented.
    turn = board.turn
    
    if turn == False: #black to move
        move = utils.rotate(move)

    # Moving a pawn to the opponent's home rank with a queen move
    # is automatically assumed to be queen underpromotion. However,
    # since queenmoves has no reference to the board and can thus not
    # determine whether the moved piece is a pawn, you have to add this
    # information manually here
    if is_queen_move:
        to_rank = chess.square_rank(move.to_square)
        is_promoting_move = (
            (to_rank == 7 and turn == True) or 
            (to_rank == 0 and turn == False)
        )

        piece = board.piece_at(move.from_square)
        if piece is None: #NOTE I added this, not entirely sure if it's correct
            return None
        is_pawn = piece.piece_type == chess.PAWN

        if is_pawn and is_promoting_move:
            move.promotion = chess.QUEEN

    return move
