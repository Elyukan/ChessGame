import pygame
from typing import TYPE_CHECKING
from enum import Enum, auto

from settings import *

if TYPE_CHECKING:
    from board import Square

class PieceType(Enum):
    POUND = "pound"
    KING = "king"
    QUEEN = "queen"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"


class PieceColor(Enum):
    BLACK = "black"
    WHITE = "white"


class Piece(pygame.sprite.Sprite):
    color: PieceColor
    piece_type: PieceType

    def __init__(self, square: "Square", pos, color: PieceColor, piece_type: PieceType) -> None:
        self._layer = 1
        self.piece_type = piece_type
        self.color = color
        super().__init__(square.board.sprite_group)
        self.image = pygame.Surface([SQUARE_SIZE / 2, SQUARE_SIZE / 2])
        color = "white" if color == color.WHITE else "black"
        self.image.fill(color=color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE + (SQUARE_SIZE / 4), pos[1] * SQUARE_SIZE + (SQUARE_SIZE / 4)
    
    def move(self, pos):
        self.rect.topleft = pos[0] * SQUARE_SIZE + (SQUARE_SIZE / 4), pos[1] * SQUARE_SIZE + (SQUARE_SIZE / 4)
        print(self.rect.topleft)
    
    def kill(self):
        super().kill()
        print("Killed")
