"""
C'est le fichier principale qui permet de lancer le jeu
"""
import pygame
from Modules.affichage import main_menu

pygame.init()
window = pygame.display.set_mode((960, 510), pygame.RESIZABLE)
color = (0, 'BLUE')

pygame.display.set_caption('Labyrinth')

logo_game = pygame.image.load("Image/logo.png")
pygame.display.set_icon(logo_game)

main_menu(window, color)
