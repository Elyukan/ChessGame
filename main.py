import sys
import pygame
from settings import *
from board import Board

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(GAME_RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.board = Board(self)

    def update(self):
        self.board.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")
        pass

    def draw(self):
        self.board.draw()
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = int(pos[0] / SQUARE_SIZE), int(pos[1] / SQUARE_SIZE)
                self.board.check_allowed_moves(pos)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()