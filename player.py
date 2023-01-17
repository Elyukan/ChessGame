import pygame
from color import Color
from board import Square, Board
from typing import List, Union
from move import Move, MoveType


class Player:
    color: Color
    selected_square: Union[Square, None]
    turn: int
    allowed_moves: List

    def __init__(self, color: Color, board: Board) -> None:
        self.board = board
        self.color = color
        self.selected_square = None
        self.turn = 1
        self.allowed_moves = []
        self.moves_regarding_pos = {}

    def select_square(self, square: Square) -> None:
        self.selected_square = square
        print(self.selected_square.pos)
        self.allowed_moves = self.board.check_allowed_moves(self)
        for move in self.allowed_moves:
            Move(self.board, move["pos"], move["type"])

    def unselect_square(self):
        self.selected_square = None
        self.board.preview_moves.empty()
        self.allowed_moves = []
        self.moves_regarding_pos = {}

    def get_selected_square(self):
        return self.selected_square

    def end_turn(self):
        self.turn += 1

    def check_if_pos_in_allowed_moves(self, pos) -> bool:
        if not self.moves_regarding_pos:
            for move in self.allowed_moves:
                self.moves_regarding_pos[move["pos"]] = move
        return bool(self.moves_regarding_pos.get(pos, False))


    # def set_allowed_moves(self):
