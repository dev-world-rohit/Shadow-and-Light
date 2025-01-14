import pygame

class Player:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.colors = [(255, 255, 255), (0, 0, 0)]
        self.color = 0
        self.collision_rect = pygame.Rect(*self.position, *self.size)

    def change_color(self):
        self.color = 1 if self.color == 0 else 0

    def display_player(self, display, offset_x, offset_y):
        pygame.draw.rect(display, self.colors[self.color], (self.position[0] + offset_x, self.position[1] + offset_y,
                                                            *self.size))