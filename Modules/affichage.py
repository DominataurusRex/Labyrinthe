import pygame
from Modules.fonction import GameStrings, Button, Button_grid, Button_image, Text, Fence
from Modules.fonction import write_game, create_new_grid, blit_grid, blit_level
from Modules.constant import COLOR_TURN, LANG, TEXTURE


game_strings = GameStrings(LANG)

def create_main_menu(window, color):
    """
    Mise en place de la logique du 'main_menu' avec:
    - 'window' la fênetre
    - 'color' la couleur
    """
    frame = pygame.Surface(window.get_size())
    play_button = Button(window, (0.35, 0.5, 0.3, 0.08),
                         game_strings.get_string('Play'), color[1])
    play_button.draw(frame)

    build_button = Button(window, (0.35, 0.6, 0.3, 0.08),
                          game_strings.get_string('Create'), color[1])
    build_button.draw(frame)

    color_text = (game_strings.get_string('Color') +
                  game_strings.get_string(color[1]))
    color_button = Button(window, (0.35, 0.7, 0.14, 0.08),
                          color_text, color[1])
    color_button.draw(frame)

    other_button = Button(window, (0.51, 0.7, 0.14, 0.08),
                          game_strings.get_string('Other'), color[1])
    other_button.draw(frame)

    exit_button = Button(window, (0.35, 0.8, 0.3, 0.08),
                         game_strings.get_string('Quit'), color[1])
    exit_button.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return play_button, build_button, color_button, other_button, exit_button


def main_menu(window, color):
    """
    Affichage du 'main_menu'
    """
    list_button_menu = create_main_menu(window, color)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_menu = create_main_menu(window, color)
            # Bouton Jouer
            if list_button_menu[0].is_pressed(event):
                print("jouer")
            # Bouton Build
            if list_button_menu[1].is_pressed(event):
                build_menu(window, color)
                create_main_menu(window, color)
            # Bouton Option
            if list_button_menu[2].is_pressed(event):
                color = (color[0] + 1, COLOR_TURN[color[0] % 4])
                create_main_menu(window, color)
            # Bouton Autre
            if list_button_menu[3].is_pressed(event):
                print("A")
            # Bouton Quitter
            if list_button_menu[4].is_pressed(event):
                pygame.quit()
                return



def create_build_menu(window, color, grid_size):
    """
    Mise en place de la logique du 'build_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid_size' le nombre de case qui doit être affiché
    """
    frame = pygame.Surface(window.get_size())

    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)

    less_button = Button(window, (0.3, 0.4, 0.1, 0.1), '-', color[1])
    less_button.draw(frame)

    grid_size_text = Text(window, (0.45, 0.4, 0.1, 0.1), grid_size)
    grid_size_text.draw(frame)

    more_button = Button(window, (0.6, 0.4, 0.1, 0.1), '+', color[1])
    more_button.draw(frame)

    enter_button = Button(window, (0.4, 0.6, 0.2, 0.1), 'Aller', color[1])
    enter_button.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return return_button, less_button, more_button, enter_button

def build_menu(window, color):
    """
    Affichage du 'build_menu'
    """
    grid_size = 10
    list_button_build = create_build_menu(window, color, grid_size)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Retour
            if list_button_build[0].is_pressed(event):
                proceed = False
            # Bouton Moins
            if list_button_build[1].is_pressed(event):
                if grid_size != 2:
                    grid_size -= 1
                    list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Plus
            if list_button_build[2].is_pressed(event):
                if grid_size != 30:
                    grid_size += 1
                    list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Entrer
            if list_button_build[3].is_pressed(event):
                tinker_menu(window, color, grid_size)
                create_build_menu(window, color, grid_size)


def create_tinker_menu(window, color, grid):
    """
    Mise en place de la logique du 'tinker_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' un 2-uple:
        - 'grid' la grille de jeu
        - 'grid_size' le nombre de case dans une ligne de la grille de jeu
    """
    frame = pygame.Surface(window.get_size())

    # Génère l'affichage du grillage
    fence = Fence(window, grid[1])

    # Prend la dimension en pixel du grillage
    dimension_grid = fence.get_dimension_grid()

    # Zone de détection du tableau
    grid_button = Button_grid(window, dimension_grid, grid[1])

    # Affiche le tableau avec les objets à l'intérieur
    frame.blit(blit_grid(window, grid, dimension_grid, TEXTURE),
                         (0, 0))

    # Bouton retour
    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)

    # Affichage du grillage
    fence.draw(frame)

    # Bordure du niveau
    blit_level(frame, color)

    # Bouton des blocs
    button1 = Button_image(frame, (0.8, 0.8, 0.1), TEXTURE[1])
    button1.draw(frame)

    window.blit(frame, (0, 0))

    pygame.display.flip()
    return return_button, grid_button


def tinker_menu(window, color, grid_size):
    """
    Affichage du 'tinker_menu'
    """
    grid = create_new_grid(grid_size)
    list_button_tinker = create_tinker_menu(window, color, (grid, grid_size))
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_tinker = create_tinker_menu(window, color, (grid, grid_size))
            # Bouton Retour
            if list_button_tinker[0].is_pressed(event):
                proceed = False
                write_game("test", grid)
            # Grille
            if list_button_tinker[1].is_pressed(event):
                print("Oui")
                coord = list_button_tinker[1].get_coord()
                grid[str(coord)]+= 1
                list_button_tinker = create_tinker_menu(window, color, (grid, grid_size))

