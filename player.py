import pygame
from color import Color
from board import Square
from typing import Union


class Player:
    color: Color
    selected_square: Union[Square, None]
    turn: int

    def __init__(self, color: Color) -> None:
        self.color = color
        self.selected_square = None
        self.turn = 1

    def select_square(self, square: Square):
        self.selected_square = square

    def unselect_square(self):
        self.selected_square = None

    def get_selected_square(self):
        return self.selected_square

    def end_turn(self):
        self.turn += 1
