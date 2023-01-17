from enum import Enum
from typing import Tuple, TYPE_CHECKING
import pygame
from settings import *


if TYPE_CHECKING:
    from board import Board

class MoveType(Enum):
    MOVE = "MOVE"
    TAKE = "TAKE"
    QUEENSIDE_CASTLE = "QUEENSIDE_CASTLE"
    KINGSIDE_CASTLE = "KINGSIDE_CASTLE"
    EN_PASSANT = "EN_PASSANT"


#TODO: Faire une class Move qui affiche et dis c'est un roque, une prise ou juste un deplacement

class Move(pygame.sprite.Sprite):
    def __init__(self, board: "Board", pos: Tuple[int, int], move_type: MoveType) -> None:
        super().__init__(board.preview_moves)
        self.pos = pos
        self.move_type = move_type
        self.image = pygame.Surface([SQUARE_SIZE / 4, SQUARE_SIZE / 4])
        if self.move_type == MoveType.TAKE:
            self.image.fill(color="red")
        else:
            self.image.fill(color="orange")
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * SQUARE_SIZE + (SQUARE_SIZE/2), pos[1] * SQUARE_SIZE + (SQUARE_SIZE/2)