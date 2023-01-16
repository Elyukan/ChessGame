import pygame
import numpy as np
from typing import Set, Union, List, Tuple, TYPE_CHECKING
from settings import *
from piece import Piece, PieceType
from color import Color


pieces = [
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
    ["pound", "pound", "pound", "pound", "pound", "pound", "pound", "pound"], 
    ["pound", "pound", "pound", "pound", "pound", "pound", "pound", "pound"],
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
]


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
        color = (217, 217, 217) if (pos[0] + pos[1]) % 2 == 0 else (40, 75, 99)
        # color = (242, 233, 228) if (pos[0] + pos[1]) % 2 == 0 else (204, 67, 61)
        self.image.fill(color=color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE
        if pos[1] <= 1:
            self.piece = Piece(self.board, pos, Color.BLACK, PieceType[pieces[pos[1]][pos[0]].upper()])
        elif pos[1] >= 6:
            self.piece = Piece(self.board, pos, Color.WHITE, PieceType[pieces[pos[1] - 4][pos[0]].upper()])
        else:
            self.piece = None

    def set_piece(self, piece: Piece):
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
        self.preview_moves = pygame.sprite.Group()
        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.board = [[Square(self, (w, h)) for w in range(WIDTH)] for h in range(HEIGHT)]
        self.game = game

    def update(self):
        self.sprite_group.update()
        self.preview_moves.update()

    def draw(self):
        self.sprite_group.draw(self.game.screen)
        self.preview_moves.draw(self.game.screen)

    def get_square(self, pos):
        return self.board[pos[1]][pos[0]]

    def check_if_piece_between_pos_and_piece(self, pos, piece: Piece):
        dx = pos[0] - piece.pos[0]
        dy = pos[1] - piece.pos[1]
        piece_pos = np.array(piece.pos)
        a_pos = np.array(pos)
        if abs(dx) == abs(dy):
            if dx > 0 and dy > 0: # bas droite
                v_pos = np.array([-1, -1])
            elif dx > 0 and dy < 0: # haut droite
                v_pos = np.array([-1, 1])
            elif dx < 0 and dy > 0: # bas gauche
                v_pos = np.array([1, -1])
            elif dx < 0 and dy < 0: # haut gauche
                v_pos = np.array([1, 1])
            # print("diag", pos)
        elif dx == 0:
            if dy > 0:
                v_pos = np.array([0, -1])
            else:
                v_pos = np.array([0, 1])
            # print("verti", pos)
        elif dy == 0:
            if dx > 0:
                v_pos = np.array([-1, 0])
            else:
                v_pos = np.array([1, 0])
        else:
            return False
        while not np.array_equal(piece_pos, a_pos):
            if self.get_square(list(a_pos)).get_piece():
                return True
            a_pos += v_pos
        return False

    def check_allowed_moves(self, piece: Piece):
        allowed_moves: Set = set()
        moves = piece.get_moves()
        for move in moves:
            if not 0 <= move[0] <= 7 or not 0 <= move[1] <= 7:
                continue
            if not self.check_if_piece_between_pos_and_piece(move, piece):
                if new_piece := self.get_square(move).get_piece():
                    if not new_piece.color == piece.color:
                        print(move)
                        allowed_moves.add(move)
                else:
                    allowed_moves.add(move)
            
        return allowed_moves