"""
Ce module s'occupe du système d'affichage des différente fenêtres
"""
import pygame

from Modules.fonction import GameStrings, Button, Buttongrid, Text, InputBox
from Modules.fonction import save_game, load_game, create_new_grid, get_dimension_grid, blit_grid
from Modules.fonction import blit_appearance, create_button_build, play_game, set_gravity, set_pos_player
from Modules.fonction import verif_level_save, verif_level_load, get_list_game
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
                proceed = False
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                list_button_menu = create_main_menu(window, color)
            # Bouton Jouer
            if list_button_menu[0].is_pressed(event):
                proceed = False
                play_menu(window, color, 'test')
                if pygame.get_init():
                    main_menu(window, color)
            # Bouton Build
            elif list_button_menu[1].is_pressed(event):
                proceed = False
                tinker_menu(window, color)
            # Bouton Option
            elif list_button_menu[2].is_pressed(event):
                color = (color[0] + 1, COLOR_TURN[color[0] % 4])
                create_main_menu(window, color)
            # Bouton Autre
            elif list_button_menu[3].is_pressed(event):
                print("A")
                verif_level_load("test3")
            # Bouton Quitter
            elif list_button_menu[4].is_pressed(event):
                proceed = False
                pygame.quit()


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

def play_menu(window, color, name_game):
    """
    Affichage du 'play_menu'
    """
    grid = load_game(name_game)
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
            # Bouton Reset
            elif list_play_menu[1].is_pressed(event):
                grid = load_game(name_game)
                gravity = 'DOWN'
                grid, pos_player = set_pos_player(grid, gravity)
                nbr_coins = 0
            if not lock:
                gravity = set_gravity(event, gravity)
        # var -> (lock, nbr_coins)
        grid, pos_player, var = play_game(grid, gravity, pos_player)
        lock = var[0]
        nbr_coins += var[1]


def create_tinker_menu(window, color, grid_size):
    """
    Mise en place de la logique du 'tinker_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid_size' le nombre de case qui doit être affiché
    """
    frame = pygame.Surface(window.get_size())

    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)

    less_button = Button(window, (0.3, 0.25, 0.1, 0.08), '-', color[1])
    less_button.draw(frame)

    grid_size_text = Text(window, (0.45, 0.25, 0.1, 0.08), grid_size)
    grid_size_text.draw(frame)

    more_button = Button(window, (0.6, 0.25, 0.1, 0.08), '+', color[1])
    more_button.draw(frame)

    create_button = Button(window, (0.3, 0.35, 0.4, 0.08),
                           game_strings.get_string('Create'), color[1])
    create_button.draw(frame)

    list_game_button = Button(window, (0.3, 0.55, 0.08, 0.18),
                              "i", color[1])
    list_game_button.draw(frame)

    load_name_input = InputBox(window, (0.4, 0.55, 0.3, 0.08), color[1])

    load_button = Button(window, (0.4, 0.65, 0.3, 0.08),
                         game_strings.get_string('Load'), color[1])
    load_button.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return (return_button, less_button, more_button, create_button,
            list_game_button, load_name_input, load_button)

def tinker_menu(window, color):
    """
    Affichage du 'tinker_menu'
    """
    name_load = ''
    grid_size = 10
    list_button_tinker = create_tinker_menu(window, color, grid_size)
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
                list_button_tinker = create_tinker_menu(window, color, grid_size)
            # Bouton Retour
            elif list_button_tinker[0].is_pressed(event):
                proceed = False
                main_menu(window, color)
            # Bouton Moins
            elif list_button_tinker[1].is_pressed(event):
                if grid_size != 5:
                    grid_size -= 1
                    list_button_tinker = create_tinker_menu(window, color, grid_size)
            # Bouton Plus
            elif list_button_tinker[2].is_pressed(event):
                if grid_size != 20:
                    grid_size += 1
                    list_button_tinker = create_tinker_menu(window, color, grid_size)
            # Bouton Creer
            elif list_button_tinker[3].is_pressed(event):
                proceed = False
                grid = create_new_grid(grid_size)
                build_menu(window, color, grid)
            # Bouton Information
            elif list_button_tinker[4].is_pressed(event):
                popup_menu(window, color, 'list_game')
                list_button_tinker = create_tinker_menu(window, color, grid_size)
            # Zone de saisie entré
            elif list_button_tinker[5].return_pressed(event):
                name_load = list_button_tinker[5].text
            # Bouton Load
            elif list_button_tinker[6].is_pressed(event):
                exit_code = verif_level_load(name_load)
                if exit_code == 0:
                    proceed = False
                    grid = load_game(name_load)
                    build_menu(window, color, grid, name_load)
                else:
                    popup_menu(window, color, 'window_exit', exit_code)
                    list_button_tinker = create_tinker_menu(window, color, grid_size)
            if proceed:
                # Zone de saisie
                list_button_tinker[5].interact(window, event)
                list_button_tinker[5].draw(window)
                pygame.display.flip()


def create_build_menu(window, color, grid, name_save):
    """
    Mise en place de la logique du 'build_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' la grille de jeu
    """
    frame = pygame.Surface(window.get_size())

    # Génère l'affichage du grillage
    dimension_grid = get_dimension_grid(frame)

    # Zone de détection du tableau
    grid_button = Buttongrid(window, dimension_grid, grid)

    # Affiche la grille de jeu
    frame.blit(blit_grid(window, grid, dimension_grid),(0, 0))

    # Bordure du niveau
    blit_appearance(frame, color)

    # Bouton des blocs
    button_block = create_button_build(frame)
    # Bouton retour
    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)
    # Bouton sauvegarde
    save_button = Button(window, (0.85, 0.05, 0.1, 0.08),
                         game_strings.get_string('Save'), color[1])
    save_button.draw(frame)

    test_button = Button(window, (0.05, 0.57, 0.1, 0.08),
                         game_strings.get_string('Test'), color[1])
    test_button.draw(frame)

    save_name_input = InputBox(window, (0.85, 0.15, 0.1, 0.08), color[1], name_save)

    window.blit(frame, (0, 0))

    pygame.display.flip()
    return return_button, save_button, grid_button, button_block, test_button, save_name_input

def build_menu(window, color, grid, name_save=''):
    """
    Affichage du 'build_menu'
    """
    list_button_build = create_build_menu(window, color, grid, name_save)
    rajout_case = 0
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
                list_button_build = create_build_menu(window, color, grid, name_save)
            # Bouton Retour
            elif list_button_build[0].is_pressed(event):
                proceed = False
                tinker_menu(window, color)
            # Bouton Sauvegarde
            elif list_button_build[1].is_pressed(event):
                exit_code = verif_level_save(grid, name_save)
                if exit_code == 0:
                    save_game(name_save, grid)
                popup_menu(window, color, 'window_exit', exit_code)
                list_button_build = create_build_menu(window, color, grid, name_save)
            # Grille
            elif list_button_build[2].is_pressed(event):
                coord = list_button_build[2].get_coord()
                if grid[str(coord)] == 0:
                    grid[str(coord)] = rajout_case
                else:
                    grid[str(coord)] = 0
                list_button_build = create_build_menu(window, color, grid, name_save)
            # Bouton Test
            elif list_button_build[4].is_pressed(event):
                exit_code = verif_level_save(grid, name_save)
                popup_menu(window, color, 'window_exit', exit_code)
                if exit_code == 0:
                    proceed = False
                    save_game(name_save, grid)
                    play_menu(window, color, name_save)
                    build_menu(window, color, grid, name_save)
                else:
                    list_button_build = create_build_menu(window, color, grid, name_save)
            # Zone de saisie entré
            elif list_button_build[5].return_pressed(event):
                name_save = list_button_build[5].text
            if proceed:
                # Button créateur
                list_touch = list_button_build[3]
                place = 1
                for button in list_touch:
                    if button.is_pressed(event):
                        rajout_case = place
                    place += 1
                # Zone de saisie
                list_button_build[5].interact(window, event)
                list_button_build[5].draw(window)
                pygame.display.flip()


def create_window_exit_menu(window, color, exit_code):
    """
    Mise en place de la logique de 'window_exit_menu' avec:
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

def create_list_game_menu(window, color):
    """
    Mise en place de la logique de 'list_game_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    """
    window_w, window_h = window.get_size()
    frame = pygame.Surface((int(window_w * 0.8), int(window_h * 0.8)))
    frame_w, frame_h = frame.get_size()
    rect = pygame.Rect(0, 0, frame_w, frame_h)
    pygame.draw.rect(frame, COLOR["BLACK"], rect)
    pygame.draw.rect(frame, COLOR[color[1]], rect, 3)

    list_game = get_list_game()
    nbr_game = 0
    for game in list_game:
        x_value = 0.01 + 0.1 * (nbr_game // 8)
        y_value = 0.01 + 0.1 * (nbr_game % 8)
        game = game.replace(".json","")
        text_game = Button(window, (x_value, y_value, 0.08, 0.08), game, color[1])
        text_game.draw(frame)
        nbr_game += 1

    window.blit(frame, (int(window_w * 0.1), int(window_h * 0.1)))
    pygame.display.flip()

def popup_menu(window, color, name_menu, other=''):
    """
    Affichage de 'popup_menu' avec comme argument:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'name_menu' pour savoir quel écran il faut afficher:
        - 'list_game' la liste des niveaux
        - 'window_exit' les messages de sorties
    - 'other' si il faut faire passer d'autre variable:
        - 'exit_code' pour la fenêtre 'window_exit'
    """
    proceed = True
    while proceed:
        if name_menu == "list_game":
            create_list_game_menu(window, color)
        elif name_menu == 'window_exit':
            create_window_exit_menu(window, color, other)
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
            # Bouton Retour
            elif event.type == pygame.MOUSEBUTTONDOWN:
                proceed = False
