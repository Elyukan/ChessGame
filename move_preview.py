import pygame
from board import Board
from settings import *


class MovePreview(pygame.sprite.Sprite):
    def __init__(self, board: Board, pos) -> None:
        super().__init__(board.preview_moves)
        self.pos = pos
        self.image = pygame.Surface([SQUARE_SIZE / 4, SQUARE_SIZE / 4])
        self.image.fill(color="orange")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE + (SQUARE_SIZE/2.6), pos[1] * SQUARE_SIZE + (SQUARE_SIZE/2.6)