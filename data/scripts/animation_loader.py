import pygame
from data.scripts.image_functions import load_image, scale_image_ratio

def load_animations(name):
    path = 'data/images/animations/' + name + '/' + name + '.txt'
    file = open(path, 'r')
    data = file.read()
    data = data.split('\n')

    animation_data = {}

    size = [0, 0]
    for info in data:
        ani_name = info.split(':')[0]
        ani_data = info.split(':')[1]

        ani_path = 'animations/' + name + '/' + ani_name
        animation = []
        for num in range(0, len(ani_data)):
            frames = ani_data[num]
            img = scale_image_ratio(load_image(ani_path + '/' + ani_name + '_' + str(num + 1) + '.png'), 0.3)
            size = [img.get_width(), img.get_height()]

            for frame in range(0, int(frames)):
                animation.append(img)
        animation_data[ani_name] = animation

    return animation_data, size
