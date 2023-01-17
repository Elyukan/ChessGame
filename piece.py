from enum import Enum
import pygame
from typing import TYPE_CHECKING

from settings import *
from color import Color

if TYPE_CHECKING:
    from board import Board

class PieceType(Enum):
    POUND = "pound"
    KING = "king"
    QUEEN = "queen"
    BISHOP = "bishop"
    KNIGHT = "knight"
    ROOK = "rook"


class Piece(pygame.sprite.Sprite):
    color: Color
    piece_type: PieceType

    def __init__(self, board: "Board", pos, color: Color, piece_type: PieceType) -> None:
        self._layer = 1
        self.piece_type = piece_type
        self.color = color
        self.pos = pos
        self.board = board
        self.already_moved = False
        super().__init__(board.sprite_group)
        self.image = pygame.image.load(f"./sprites/pieces/{color.value}-{piece_type.value}.png")
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE
    
    def move(self, pos):
        self.rect.topleft = pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE
        self.pos = pos
        self.already_moved = True
    
    def kill(self):
        super().kill()
        print("Killed")

    def get_moves(self):
        moves = []
        if self.piece_type == PieceType.POUND:
            if self.color == Color.WHITE:
                moves.extend([(self.pos[0], self.pos[1] - 1)])
                if not self.already_moved:
                    moves.append((self.pos[0], self.pos[1] - 2))
                if 0 <= self.pos[0] - 1 <= 7 and 0 <= self.pos[1] - 1 <= 7:
                    if piece := self.board.get_square((self.pos[0] - 1, self.pos[1] - 1)).get_piece():
                        if piece.color == Color.BLACK:
                            moves.append((self.pos[0] - 1, self.pos[1] - 1))
                if 0 <= self.pos[0] + 1 <= 7 and 0 <= self.pos[1] - 1 <= 7:
                    if piece := self.board.get_square((self.pos[0] + 1, self.pos[1] - 1)).get_piece():
                        if piece.color == Color.BLACK:
                            moves.append((self.pos[0] + 1, self.pos[1] - 1))
            else:
                moves.extend([(self.pos[0], self.pos[1] + 1)])
                if not self.already_moved:
                    moves.append((self.pos[0], self.pos[1] + 2))
                if 0 <= self.pos[0] + 1 <= 7 and 0 <= self.pos[1] + 1 <= 7:
                    if piece := self.board.get_square((self.pos[0] + 1, self.pos[1] + 1)).get_piece():
                        if piece.color == Color.WHITE:
                            moves.append((self.pos[0] + 1, self.pos[1] + 1))
                if 0 <= self.pos[0] - 1 <= 7 and 0 <= self.pos[1] + 1 <= 7:
                    if piece := self.board.get_square((self.pos[0] - 1, self.pos[1] + 1)).get_piece():
                        if piece.color == Color.WHITE:
                            moves.append((self.pos[0] - 1, self.pos[1] + 1))
        if self.piece_type == PieceType.KNIGHT:
            moves.extend([
                (self.pos[0] + 1, self.pos[1] + 2),
                (self.pos[0] + 1, self.pos[1] - 2),
                (self.pos[0] - 1, self.pos[1] - 2),
                (self.pos[0] - 1, self.pos[1] + 2),
                (self.pos[0] - 2, self.pos[1] + 1),
                (self.pos[0] - 2, self.pos[1] - 1),
                (self.pos[0] + 2, self.pos[1] - 1),
                (self.pos[0] + 2, self.pos[1] + 1)
            ])
        if self.piece_type in [PieceType.ROOK, PieceType.QUEEN]:
            moves.extend([(self.pos[0] + i, self.pos[1]) for i in range(-WIDTH, WIDTH) if i != 0])
            moves.extend([(self.pos[0], self.pos[1] + i) for i in range(-HEIGHT, HEIGHT) if i != 0])
        if self.piece_type in [PieceType.BISHOP, PieceType.QUEEN]:
            moves.extend([(self.pos[0] + i, self.pos[1] + i) for i in range(-WIDTH, WIDTH) if i != 0])
            moves.extend([(self.pos[0] - i, self.pos[1] - i) for i in range(-HEIGHT, HEIGHT) if i != 0])
            moves.extend([(self.pos[0] + i, self.pos[1] - i) for i in range(-HEIGHT, HEIGHT) if i != 0])
            moves.extend([(self.pos[0] - i, self.pos[1] + i) for i in range(-HEIGHT, HEIGHT) if i != 0])
        if self.piece_type == PieceType.KING:
            moves.extend(
                [
                    (self.pos[0] + 1, self.pos[1] + 1),
                    (self.pos[0] + 1, self.pos[1]),
                    (self.pos[0] + 1, self.pos[1] - 1),
                    (self.pos[0] - 1, self.pos[1] - 1),
                    (self.pos[0] - 1, self.pos[1] + 1),
                    (self.pos[0] - 1, self.pos[1]),
                    (self.pos[0], self.pos[1] + 1),
                    (self.pos[0], self.pos[1] - 1),
                ]
            )
        return moves
