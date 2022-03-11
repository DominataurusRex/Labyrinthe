import pygame

pygame.init()

window = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)


def fenetre():
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                window_surface = window.get_size()
                color = (0, 59, 111) 
                pygame.draw.rect(window, color, pygame.Rect(window_surface[0]*0.25, window_surface[1]*0.25, window_surface[0]*0.5, window_surface[1]*0.5))
        pygame.display.flip()


fenetre()