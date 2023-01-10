import pygame
from typing import Union, List, Tuple, TYPE_CHECKING
from settings import *
from piece import Piece, PieceColor, PieceType


if TYPE_CHECKING:
    from main import Game


class Square(pygame.sprite.Sprite):
    piece: Union[Piece, None]

    def __init__(self, board: "Board", pos: Tuple[int, int]) -> None:
        self._layer = 0
        self.board = board
        super().__init__(board.sprite_group)
        self.pos = pos
        self.image = pygame.Surface([SQUARE_SIZE, SQUARE_SIZE])
        color = (60, 60, 60) if (pos[0] + pos[1]) % 2 == 0 else (66, 33, 0)
        self.image.fill(color=color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE
        if pos[1] <= 1:
            self.piece = Piece(self, pos, PieceColor.BLACK, PieceType.POUND)
        elif pos[1] >= 6:
            self.piece = Piece(self, pos, PieceColor.WHITE, PieceType.POUND)
        else:
            self.piece = None

    def set_piece(self,piece: Piece):
        if self.piece and piece:
            print("here")
            self.piece.kill()
        if piece:
            piece.move(self.pos)
        self.piece = piece

    def get_piece(self):
        return self.piece


class Board:
    board: List[List[Square]]

    def __init__(self, game: "Game") -> None:
        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.board = [[Square(self, (w, h)) for w in range(WIDTH)] for h in range(HEIGHT)]
        self.game = game

    def update(self):
        self.sprite_group.update()

    def draw(self):
        self.sprite_group.draw(self.game.screen)

    def get_square(self, pos):
        return self.board[pos[1]][pos[0]]

    def check_allowed_moves(self, pos):
        selected_square = self.get_square(pos)
        if selected_piece := selected_square.get_piece():
            if selected_piece.color == PieceColor.BLACK:
                new_pos = pos[0], pos[1] + 1
            else:
                new_pos = pos[0], pos[1] - 1
            new_square = self.get_square(new_pos)
            new_square.set_piece(selected_piece)
            selected_square.set_piece(None)

