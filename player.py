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

    def select_square(self, square: Square):
        self.selected_square = square
        print(self.selected_square.pos)
        moves = self.selected_square.get_piece().get_moves()
        for move in moves:
            MovePreview(self.board, move)

    def unselect_square(self):
        self.selected_square = None
        self.board.preview_moves.empty()

    def get_selected_square(self):
        return self.selected_square

    def end_turn(self):
        self.turn += 1

    # def set_allowed_moves(self):
