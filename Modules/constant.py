"""
Ce module s'occupe des constante utiliser dans les autres modules
"""
import pygame

COLOR = {'BLUE': (0, 59, 111),
         'DARK_BLUE': (0, 22, 43),
         'GREEN': (34, 120, 15),
         'DARK_GREEN': (17, 61, 7),
         'YELLOW': (255, 215, 0),
         'DARK_YELLOW': (170, 145, 0),
         'RED': (207, 10, 29),
         'DARK_RED': (101, 5, 15),
         'WHITE': (255, 255, 255),
         'GRAY': (96, 96, 96),
         'DARK_GRAY': (47, 47, 47),
         'BLACK': (0, 0, 0)}

COLOR_TURN = ['GREEN', 'YELLOW', 'RED', 'BLUE']

LANG = 'En'

FONT_HEIGHT = [19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 35, 37,
               38, 40, 41, 43, 44, 46, 47, 49, 50, 52, 53, 55, 56,
               58, 59, 61, 62, 64, 65, 67, 68, 70, 71, 73, 74, 76,
               77, 79, 80, 82, 83, 85, 86, 88, 89, 91, 92, 94, 95,
               97, 98, 100, 101, 103, 104, 106, 107, 109, 110, 112,
               113, 115, 116, 118, 119, 121, 122, 124, 125, 127, 128,
               130, 131, 133, 134, 136, 137, 139, 140, 142, 144, 145,
               147, 148, 150, 151, 153, 154, 156, 157, 159, 160, 162,
               163, 165, 166, 168, 169, 171, 172, 174, 175, 177, 178,
               180, 181, 183, 184, 186, 187, 189, 190, 192, 193, 195,
               196, 198, 199, 201, 202, 204, 205, 207, 208, 210, 211,
               213, 214, 216, 217, 219, 220, 222, 223, 225, 226, 228,
               229, 231, 232, 234, 235, 237, 238, 240, 241, 243, 244,
               246, 247, 249, 250, 252, 253, 255, 256, 258, 259, 261,
               262, 264, 265, 267, 268, 270, 271, 273, 274, 276, 277,
               279, 280, 282, 284, 285, 287, 288, 290, 291, 293, 294,
               296, 297, 299, 300]

# Initialise les images
def level_init():
    """
    Permet de précharger toute les textures au lancement du jeu
    """
    image = pygame.image.load("Image/level_texture.png")
    x_value = image.get_width()
    y_value = image.get_height()
    place = -4
    texture = {}
    for height in range(y_value // 32):
        for width in range(x_value // 32):
            image_temp = image.subsurface((32 * width, 32 * height, 32, 32))
            texture[place] = image_temp
            place += 1
    image_charac = pygame.image.load("Image/character.png")
    texture['DOWN'] = image_charac.subsurface((0, 0, 32, 32))
    texture['LEFT'] = image_charac.subsurface((32, 0, 32, 32))
    texture['RIGHT'] = image_charac.subsurface((0, 32, 32, 32))
    texture['UP'] = image_charac.subsurface((32, 32, 32, 32))
    texture['compass_DOWN'] = pygame.image.load("Image/arrow_down.png")
    texture['compass_LEFT'] = pygame.image.load("Image/arrow_left.png")
    texture['compass_RIGHT'] = pygame.image.load("Image/arrow_right.png")
    texture['compass_UP'] = pygame.image.load("Image/arrow_up.png")
    return texture

TEXTURE = level_init()
