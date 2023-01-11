from enum import Enum
import pygame
from typing import TYPE_CHECKING

from settings import *

if TYPE_CHECKING:
    from board import Square
    from color import Color

class PieceType(Enum):
    POUND = "pound"
    KING = "king"
    QUEEN = "queen"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"


class Piece(pygame.sprite.Sprite):
    color: "Color"
    piece_type: PieceType

    def __init__(self, square: "Square", pos, color: "Color", piece_type: PieceType) -> None:
        self._layer = 1
        self.piece_type = piece_type
        self.color = color
        self.pos = pos
        super().__init__(square.board.sprite_group)
        self.image = pygame.Surface([SQUARE_SIZE / 2, SQUARE_SIZE / 2])
        self.image.fill(color=self.color.value)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE + (SQUARE_SIZE / 4), pos[1] * SQUARE_SIZE + (SQUARE_SIZE / 4)
    
    def move(self, pos):
        self.rect.topleft = pos[0] * SQUARE_SIZE + (SQUARE_SIZE / 4), pos[1] * SQUARE_SIZE + (SQUARE_SIZE / 4)
        self.pos = pos
    
    def kill(self):
        super().kill()
        print("Killed")
