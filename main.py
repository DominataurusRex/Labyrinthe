import pygame
from Modules.affichage import main_menu
from Modules.fonction import init_texture

pygame.init()
window = pygame.display.set_mode((960, 510), pygame.RESIZABLE)
color = (0, 'BLUE')

texture = init_texture(window)
main_menu(window, texture, color)
