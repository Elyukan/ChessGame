import pygame
from color import Color
from board import Square, Board
from typing import List, Union
from move_preview import MovePreview


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

    def select_square(self, square: Square):
        self.selected_square = square
        print(self.selected_square.pos)
        self.allowed_moves = self.board.check_allowed_moves(self.selected_square.get_piece())
        for move in self.allowed_moves:
            MovePreview(self.board, move)

    def unselect_square(self):
        self.selected_square = None
        self.board.preview_moves.empty()
        self.allowed_moves = []

    def get_selected_square(self):
        return self.selected_square

    def end_turn(self):
        self.turn += 1

    # def set_allowed_moves(self):
