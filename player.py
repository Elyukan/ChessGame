import pygame
from enum import Enum, auto


class PlayerColor(Enum):
    BLACK: auto
    WHITE: auto


class Player:
    color: PlayerColor
