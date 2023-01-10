import pygame
from enum import Enum, auto


class PieceType(Enum):
    POUND: auto
    KING: auto
    QUEEN: auto
    BISHOP: auto
    KNIGHT: auto
    ROOK: auto


class PieceColor(Enum):
    BLACK: auto
    WHITE: auto


class Piece:
    color: PieceColor
    piece_type: PieceType
