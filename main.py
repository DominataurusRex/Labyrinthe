import pygame
from Modules.affichage import main_menu

pygame.init()
window = pygame.display.set_mode((960, 510), pygame.RESIZABLE)
color = (0, 'BLUE')

main_menu(window, color)
