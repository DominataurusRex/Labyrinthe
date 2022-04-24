from time import sleep
import pygame

from Modules.fonction import GameStrings, Button, Button_grid, Text
from Modules.fonction import save_game, load_game, create_new_grid, get_dimension_grid, blit_grid
from Modules.fonction import blit_appearance, create_button_tinker, play_game, set_gravity, set_pos_player
from Modules.fonction import verif_level_save
from Modules.constant import COLOR, COLOR_TURN, LANG


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
            elif event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_menu = create_main_menu(window, color)
            # Bouton Jouer
            if list_button_menu[0].is_pressed(event):
                proceed = False
                play_menu(window, color)
            # Bouton Build
            elif list_button_menu[1].is_pressed(event):
                proceed = False
                build_menu(window, color)
            # Bouton Option
            elif list_button_menu[2].is_pressed(event):
                color = (color[0] + 1, COLOR_TURN[color[0] % 4])
                create_main_menu(window, color)
            # Bouton Autre
            elif list_button_menu[3].is_pressed(event):
                print("A")
            # Bouton Quitter
            elif list_button_menu[4].is_pressed(event):
                pygame.quit()
                return


def create_play_menu(window, color, grid, nbr_coins):
    """
    Mise en place de la logique du 'play_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    """
    frame = pygame.Surface(window.get_size())
    dimension_grid = get_dimension_grid(frame)
    frame.blit(blit_grid(window, grid, dimension_grid),(0, 0))
    blit_appearance(frame, color)

    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)

    reset_button = Button(window, (0.85, 0.05, 0.1, 0.08),
                          game_strings.get_string('Reset'), color[1])
    reset_button.draw(frame)

    coin_display = Text(window, (0.2, 0.7, 0.08, 0.1), str(nbr_coins) + "x pt")
    coin_display.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return return_button, reset_button

def play_menu(window, color):
    """
    Affichage du 'play_menu'
    """
    grid = load_game('test')
    gravity = 'DOWN'
    grid, pos_player = set_pos_player(grid, gravity)
    nbr_coins = 0
    proceed = True
    lock = False
    while proceed:
        list_play_menu = create_play_menu(window, color, grid, nbr_coins)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
            # Bouton Quitter
            elif list_play_menu[0].is_pressed(event):
                proceed = False
                main_menu(window, color)
            # Bouton Reset
            elif list_play_menu[1].is_pressed(event):
                grid = load_game('test')
                gravity = 'DOWN'
                grid, pos_player = set_pos_player(grid, gravity)
                nbr_coins = 0
            if not lock:
                gravity = set_gravity(event, gravity)
        # var -> (lock, nbr_coins)
        grid, pos_player, var = play_game(grid, gravity, pos_player)
        lock = var[0]
        nbr_coins += var[1]
        


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

    less_button = Button(window, (0.3, 0.4, 0.1, 0.08), '-', color[1])
    less_button.draw(frame)

    grid_size_text = Text(window, (0.45, 0.4, 0.1, 0.08), grid_size)
    grid_size_text.draw(frame)

    more_button = Button(window, (0.6, 0.4, 0.1, 0.08), '+', color[1])
    more_button.draw(frame)

    create_button = Button(window, (0.4, 0.6, 0.2, 0.08), 
                           game_strings.get_string('Create'), color[1])
    create_button.draw(frame)

    load_button = Button(window, (0.4, 0.7, 0.2, 0.08),
                         game_strings.get_string('Load'), color[1])
    load_button.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return return_button, less_button, more_button, create_button, load_button

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
            elif event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Retour
            elif list_button_build[0].is_pressed(event):
                proceed = False
                main_menu(window, color)
            # Bouton Moins
            elif list_button_build[1].is_pressed(event):
                if grid_size != 5:
                    grid_size -= 1
                    list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Plus
            elif list_button_build[2].is_pressed(event):
                if grid_size != 20:
                    grid_size += 1
                    list_button_build = create_build_menu(window, color, grid_size)
            # Bouton Creer
            elif list_button_build[3].is_pressed(event):
                proceed = False
                grid = create_new_grid(grid_size)
                tinker_menu(window, color, grid)
            # Bouton Load
            elif list_button_build[4].is_pressed(event):
                proceed = False
                grid = load_game('test')
                tinker_menu(window, color, grid)


def create_tinker_menu(window, color, grid):
    """
    Mise en place de la logique du 'tinker_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' la grille de jeu
    """
    frame = pygame.Surface(window.get_size())

    # Génère l'affichage du grillage
    dimension_grid = get_dimension_grid(frame)
    
    # Zone de détection du tableau
    grid_button = Button_grid(window, dimension_grid, grid)

    # Affiche la grille de jeu
    frame.blit(blit_grid(window, grid, dimension_grid),(0, 0))

    # Bordure du niveau
    blit_appearance(frame, color)

    # Bouton des blocs
    button_block = create_button_tinker(frame)
    # Bouton retour
    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)
    # Bouton sauvegarde
    save_button = Button(window, (0.85, 0.05, 0.1, 0.08),
                         game_strings.get_string('Save'), color[1])
    save_button.draw(frame)

    window.blit(frame, (0, 0))

    pygame.display.flip()
    return return_button, save_button, grid_button, button_block

def tinker_menu(window, color, grid):
    """
    Affichage du 'tinker_menu'
    """
    list_button_tinker = create_tinker_menu(window, color, grid)
    proceed = True
    rajout_case = 0
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_tinker = create_tinker_menu(window, color, grid)
            # Bouton Retour
            elif list_button_tinker[0].is_pressed(event):
                proceed = False
                build_menu(window, color)
            # Bouton Sauvegarde
            elif list_button_tinker[1].is_pressed(event):
                exit_code = verif_level_save(grid)
                if exit_code == 1:
                    save_game("test", grid)
                save_menu(window, color, exit_code)
                sleep(2)
                list_button_tinker = create_tinker_menu(window, color, grid)
            # Grille
            elif list_button_tinker[2].is_pressed(event):
                coord = list_button_tinker[2].get_coord()
                if grid[str(coord)] == 0:
                    grid[str(coord)] = rajout_case
                else:
                    grid[str(coord)] = 0
                list_button_tinker = create_tinker_menu(window, color, grid)
            # Button créateur
            if proceed:
                list_touch = list_button_tinker[3]
                place = 1
                for button in list_touch:
                    if button.is_pressed(event):
                        rajout_case = place
                    place += 1

def save_menu(window, color, exit_code):
    """
    Mise en place de la logique du 'save_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'exit_code' le code de sortie de la sauvegarde
    """
    window_w, window_h = window.get_size()
    frame = pygame.Surface((int(window_w * 0.4), int(window_h * 0.2)))
    frame_w, frame_h = frame.get_size()
    rect = pygame.Rect(0, 0, frame_w, frame_h)
    pygame.draw.rect(frame, COLOR["DARK_" + color[1]], rect)
    pygame.draw.rect(frame, COLOR[color[1]], rect, 3)

    exit_text = Text(frame, (0, 0.25, 1, 0.5),
                     game_strings.get_string('Exit_code_' + str(exit_code)))
    exit_text.draw(frame)


    window.blit(frame, (int(window_w * 0.3), int(window_h * 0.4)))
    pygame.display.flip()