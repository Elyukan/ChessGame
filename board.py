import pygame
from typing import Union, List, Tuple, TYPE_CHECKING
from settings import *
from enum import Enum, auto
from piece import Piece


if TYPE_CHECKING:
    from main import Game


class SquareColor(Enum):
    BLACK: auto
    WHITE: auto


class Square(pygame.sprite.Sprite):
    piece: Union[Piece, None]

    def __init__(self, board: "Board", pos: Tuple[int, int]) -> None:
        self.board = board
        super().__init__(board.sprite_group)
        self.image = pygame.Surface([SQUARE_SIZE, SQUARE_SIZE])
        color = "white" if (pos[0] + pos[1]) % 2 == 0 else "black"
        self.image.fill(color=color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE
        self.piece = None


class Board:
    board: List[List[Square]]

    def __init__(self, game: "Game") -> None:
        self.sprite_group = pygame.sprite.Group()
        self.board = [[Square(self, (w, h)) for w in range(WIDTH)] for h in range(HEIGHT)]
        self.game = game

    def update(self):
        self.sprite_group.update()

    def draw(self):
        self.sprite_group.draw(self.game.screen)

