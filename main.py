import webbrowser

import pygame
import random
from pygame.locals import *

from data.scripts.animation_player import AnimationPlayer
from data.scripts.circles import Circle
from data.scripts.player import Player
from data.scripts.font import Font
from data.scripts.image_functions import load_image, scale_image_ratio, scale_image_size

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow and Light")
icon = load_image('shot.png')
pygame.display.set_icon(icon)

# Images-----------------------------#
white_overlay = scale_image_size(load_image('white_background_overlay.png', 30), SCREEN_WIDTH, SCREEN_HEIGHT)

road_background = load_image('road_background.png')

heart = load_image('heart.png')
heart = scale_image_ratio(heart, 2)

button_scale = 0.8
yellow_music_on_button = scale_image_ratio(load_image('buttons/black_buttons/yellow_music_on.png'), button_scale)
yellow_music_off_button = scale_image_ratio(load_image('buttons/black_buttons/yellow_music_off.png'), button_scale)
yellow_play_button = scale_image_ratio(load_image('buttons/black_buttons/yellow_play.png'), button_scale)
yellow_thumbs_up_button = scale_image_ratio(load_image('buttons/black_buttons/yellow_thumbs_up.png'), button_scale)

white_music_on_button = scale_image_ratio(load_image('buttons/white_buttons/white_music_on.png'), button_scale)
white_music_off_button = scale_image_ratio(load_image('buttons/white_buttons/white_music_off.png'), button_scale)
white_play_button = scale_image_ratio(load_image('buttons/white_buttons/white_play.png'), button_scale)
white_thumbs_up_button = scale_image_ratio(load_image('buttons/white_buttons/white_thumbs_up.png'), button_scale)

buttons = {
    'music_on': [yellow_music_on_button, white_music_on_button, [SCREEN_WIDTH - 50, 10]],
    'music_off': [yellow_music_off_button, white_music_off_button, [SCREEN_WIDTH - 50, 10]],
    'play': [yellow_play_button, white_play_button, [(SCREEN_WIDTH - yellow_play_button.get_width()) // 2 -
                                                    yellow_play_button.get_width(),
                                                    (SCREEN_HEIGHT - yellow_play_button.get_height()) // 2]],
    'thumbs_up': [yellow_thumbs_up_button, white_thumbs_up_button, [(SCREEN_WIDTH - yellow_play_button.get_width())
                                                                      // 2 + yellow_play_button.get_width(),
                                                    (SCREEN_HEIGHT - yellow_play_button.get_height()) // 2]]
}

# Music-----------------------------#
def load_sound(file_name):
    return pygame.mixer.Sound("data/audio/" + file_name)

def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# pygame.mixer.Sound.set_volume(1)
explosion = load_sound('pop.wav')
failed = load_sound('fail.wav')

background_music = pygame.mixer.music.load('data/audio/background_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)


def apply_shake(shake_duration):
    if shake_duration > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        return offset_x, offset_y
    return 0, 0

# Text-----------------------------#
text = Font('large_font.png', (255, 255, 255), 2)
main_menu_text = Font('large_font.png', (10, 0, 0), 1.5)

# Constants-----------------------------#
clock = pygame.time.Clock()
FPS = 60


player_size = [200, 50]
player = Player([(SCREEN_WIDTH - player_size[0]) // 2, SCREEN_HEIGHT - player_size[1] * 5], player_size)

explosion_animation = AnimationPlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size[1] * 5)
explosion_animation.animations('explosion')

circle_radius = 20
circle_distance = 250
circle_numbers = 7
circles = []

shake_duration = 0
shake_intensity = 10

road_color = (74, 113, 129)
road_width, road_height = road_background.get_size()
background_color = (52, 96, 114)
road_x = (SCREEN_WIDTH - road_width) // 2
road_y = 0
roads = [0, -road_height]
road_speed = 3

score_x, score_y = 10, 10
score = 0

button_click = False
button_clicked = None

music_on = True

game_start = True

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    if game_start:
        circles = [Circle([SCREEN_WIDTH // 2, -circle_distance * i], random.choice([0, 1]), circle_radius) for i in
                   range(circle_numbers)]
        score = 0
        circle_distance = 250
        road_speed = 3
        setattr(Circle, 'speed', 2)
        if button_click:
            button_click = False
            if button_clicked == 'music_on':
                music_on = False
                pygame.mixer.music.stop()
            if button_clicked == 'music_off':
                music_on = True
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.8)
            if button_clicked == 'play':
                game_start = False
            if button_clicked == 'thumbs_up':
                webbrowser.open('https://github.com/dev-world-rohit')

    offset_x, offset_y = apply_shake(shake_duration)

    screen.fill(background_color)

    pygame.draw.rect(screen, road_color, (road_x + offset_x, 0 + offset_y, road_width, SCREEN_HEIGHT))

    for i in range(2):
        screen.blit(road_background, (road_x + offset_x, road_y + offset_y + roads[i]))
        roads[i] += road_speed
        if roads[i] > road_height:
            roads[i] = -road_height

    screen.blit(heart, [score_x + offset_x, score_y + offset_y])
    text.display_fonts(screen, f"{score}", [heart.get_width() + score_x + 5 + offset_x, 15 + offset_y], 2)

    explosion_animation.play_animation(screen, [offset_x, offset_y])

    if not game_start:
        for circle in circles:
            circle.display_circle(screen, offset_x, offset_y)
            if player.collision_rect.colliderect(circle.collision_rect):
                if circle.color == player.color:
                    circle.position[1] = min(c.position[1] for c in circles) - circle_distance
                    circle.color = random.choice([0, 1])
                    score += 1
                    shake_duration = 10
                    explosion_animation.start_animation = True
                    play_sound(explosion)
                    if score > 1 and score % 10 == 0:
                        circle_distance -= 10
                        setattr(Circle, 'speed', Circle.speed + 0.5)
                else:
                    play_sound(failed)
                    shake_duration = 20
                    game_start = True

    player.display_player(screen, offset_x, offset_y)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if not game_start:
                player.change_color()
            else:
                button_click = True
                #game_start = False

    if shake_duration > 0:
        shake_duration -= 1

    if game_start:
        screen.blit(white_overlay, (0, 0))
        for button in buttons:
            if music_on and button == 'music_off':
                continue
            if not music_on and button == 'music_on':
                continue

            button_data = buttons[button]
            if (button_data[2][0] < mouse_pos[0] < button_data[2][0] + button_data[0].get_width() and button_data[2][1] < mouse_pos[1]
                    < button_data[2][1] + button_data[0].get_height()):
                screen.blit(button_data[1], button_data[2])
                button_clicked = button
            else:
                screen.blit(button_data[0], button_data[2])

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
