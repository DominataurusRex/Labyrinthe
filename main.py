import pygame
from Modules.affichage import main_menu

pygame.init()
window = pygame.display.set_mode((960, 510), pygame.RESIZABLE)
color = (0, 'BLUE')

def temp():
    liste = []
    for ligne in range(10):
        temp = []
        for colonne in range(10):
            temp.append('0')
        liste.append(temp)
    for l in liste:
        print(l)

main_menu(window, color)
