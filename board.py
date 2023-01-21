import pygame
import numpy as np
from typing import Set, Union, List, Tuple, TYPE_CHECKING
from settings import *
from piece import Piece, PieceType
from color import Color
from move import MoveType

if TYPE_CHECKING:
    from player import Player


pieces = [
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
    ["pound", "pound", "pound", "pound", "pound", "pound", "pound", "pound"], 
    ["pound", "pound", "pound", "pound", "pound", "pound", "pound", "pound"],
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
]


if TYPE_CHECKING:
    from main import Game

#TODO: Faire en sorte que quand la case est selectionnée, elle change de couleur

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

    def set_piece(self, piece: Piece) -> None:
        if self.piece and piece:
            print("here")
            self.piece.kill()
        if piece:
            piece.move(self.pos)
        self.piece = piece

    def get_piece(self) -> Union[Piece, None]:
        return self.piece


class Board:
    board: List[List[Square]]

    def __init__(self, game: "Game") -> None:
        self.preview_moves = pygame.sprite.Group()
        self.sprite_group = pygame.sprite.LayeredUpdates()
        self.board = [[Square(self, (w, h)) for w in range(WIDTH)] for h in range(HEIGHT)]
        self.game = game

    def update(self) -> None:
        self.sprite_group.update()
        self.preview_moves.update()

    def draw(self) -> None:
        self.sprite_group.draw(self.game.screen)
        self.preview_moves.draw(self.game.screen)

    def get_square(self, pos) -> Square:
        return self.board[pos[1]][pos[0]]

    def check_if_piece_between_pos_and_piece(self, pos: Tuple[int, int], piece: Piece) -> bool:
        if piece.piece_type == PieceType.KNIGHT:
            return False
        dx = pos[0] - piece.pos[0]
        dy = pos[1] - piece.pos[1]
        piece_pos = np.array(piece.pos)
        target_pos = np.array(pos)
        if abs(dx) == abs(dy):
            if dx > 0 and dy > 0: # bas droite
                v_pos = np.array([1, 1])
            elif dx > 0 and dy < 0: # haut droite
                v_pos = np.array([1, -1])
            elif dx < 0 and dy > 0: # bas gauche
                v_pos = np.array([-1, 1])
            elif dx < 0 and dy < 0: # haut gauche
                v_pos = np.array([-1, -1])
        elif dx == 0:
            if dy > 0:
                v_pos = np.array([0, 1])
            else:
                v_pos = np.array([0, -1])
        elif dy == 0:
            if dx > 0:
                v_pos = np.array([1, 0])
            else:
                v_pos = np.array([-1, 0])
        else:
            return False
        is_piece = False
        while not np.array_equal(piece_pos, target_pos):
            piece_pos += v_pos
            if is_piece:
                return True
            if self.get_square(list(piece_pos)).get_piece():
                is_piece = True
        return False

    def add_castle_moves(self, player: "Player", piece: Piece) -> List:
        castle_moves = []
        if self.check_if_queenside_castle(player, piece):
            if player.color == Color.BLACK:
                castle_moves.append({"pos": (2, 0), "type": MoveType.QUEENSIDE_CASTLE})
            elif player.color == Color.WHITE:
                castle_moves.append({"pos": (2, 7), "type": MoveType.QUEENSIDE_CASTLE})
        if self.check_if_kingside_castle(player, piece):
            if player.color == Color.BLACK:
                castle_moves.append({"pos": (6, 0), "type": MoveType.KINGSIDE_CASTLE})
            elif player.color == Color.WHITE:
                castle_moves.append({"pos": (6, 7), "type": MoveType.KINGSIDE_CASTLE})
        return castle_moves

    def check_if_queenside_castle(self, player: "Player", king: Piece) -> bool:
        if king.already_moved:
            return False
        if player.color == Color.BLACK:
            rook_pos = (0, 0)
        else:
            rook_pos = (0, 7)
        if not (rook := self.get_square(rook_pos).get_piece()):
            return False
        if rook.already_moved:
            return False
        if self.check_if_piece_between_pos_and_piece(rook_pos, king):
            return False
        return True

    def check_if_kingside_castle(self, player: "Player", king: Piece) -> bool:
        if king.already_moved:
            return False
        if player.color == Color.BLACK:
            rook_pos = (7, 0)
        else:
            rook_pos = (7, 7)
        if not (rook := self.get_square(rook_pos).get_piece()):
            return False
        if rook.already_moved:
            return False
        if self.check_if_piece_between_pos_and_piece(rook_pos, king):
            return False
        return True

    def check_allowed_moves(self, player: "Player") -> Set:
        allowed_moves: List = []
        piece: Piece = player.selected_square.get_piece()
        moves = piece.get_moves()
        for move in moves:
            if not 0 <= move[0] <= 7 or not 0 <= move[1] <= 7:
                continue
            if self.check_if_piece_between_pos_and_piece(move, piece):
                continue
            elif new_piece := self.get_square(move).get_piece():
                if piece.piece_type == PieceType.POUND:
                    if new_piece.pos[0] == piece.pos[0] and (new_piece.pos[1] - 1 == piece.pos[1] or new_piece.pos[1] + 1 == piece.pos[1]):
                        continue
                if not new_piece.color == piece.color:
                    allowed_moves.append({"pos": move, "type": MoveType.TAKE})
            else:
                allowed_moves.append({"pos": move, "type": MoveType.MOVE})
        if piece.piece_type == PieceType.KING:
            allowed_moves.extend(self.add_castle_moves(player, piece))
        #TODO: Check si la piece est clouée

        #TODO: Check si le roi est en echec
        return allowed_moves