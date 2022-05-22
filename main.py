"""
C'est le fichier principale qui permet de lancer le jeu
"""
import pygame
from Modules.affichage import main_menu

pygame.init()
window = pygame.display.set_mode((960, 510), pygame.RESIZABLE)

pygame.display.set_caption('Maze Maker')

icon_game = pygame.image.load("Image/icon.png")
pygame.display.set_icon(icon_game)

main_menu(window)
