import sys
import pygame
from settings import *
from board import Board
from player import Player
from color import Color

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(GAME_RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.board = Board(self)
        self.white_player = Player(Color.WHITE)
        self.black_player = Player(Color.BLACK)
        self.turn = 1
        self.player_to_play = self.white_player

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
                selected_square = self.board.get_square(pos)
                if not self.player_to_play.get_selected_square():
                    if selected_piece := selected_square.get_piece():
                        if self.player_to_play.color == selected_piece.color:
                            self.player_to_play.select_square(selected_square)
                else:
                    old_selected_square = self.player_to_play.get_selected_square()
                    if selected_square != old_selected_square:
                        selected_piece = old_selected_square.get_piece()
                        selected_square.set_piece(selected_piece)
                        old_selected_square.set_piece(None)
                        self.player_to_play.end_turn()
                    self.player_to_play.unselect_square()
                    
    
    def check_turn(self):
        if self.player_to_play == self.white_player:
            if self.white_player.turn > self.turn:
                self.player_to_play = self.black_player
        if self.player_to_play == self.black_player:
            if self.black_player.turn > self.turn:
                self.turn += 1
                self.player_to_play = self.white_player


    def run(self):
        while True:
            self.check_turn()
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()