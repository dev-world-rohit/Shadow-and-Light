import pygame

class Circle:
    speed = 2
    def __init__(self, position, color_number, radius):
        self.position = position
        self.color = color_number
        self.colors = [(255, 255, 255), (0, 0, 0)]
        self.combo_colors = [(200, 200, 200), (50, 50, 50)]
        self.radius = radius
        self.collision_rect = pygame.Rect(self.position[0] - self.radius, self.position[1] - self.radius * 2,
                                          2 * self.radius, self.radius)

    def move(self):
        self.position[1] += int(self.speed)
        self.collision_rect.y = self.position[1]

    def display_circle(self, display, offset_x, offset_y):
        self.move()
        pygame.draw.circle(display, self.colors[self.color], (self.position[0] + offset_x, self.position[1] + offset_y),
                           self.radius)
        pygame.draw.circle(display, self.combo_colors[self.color], (self.position[0] + offset_x, self.position[1] + offset_y), self.radius - 5)
