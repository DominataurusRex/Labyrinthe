"""
Ce module s'occupe du système d'affichage des différente fenêtres
"""
import pygame

from Modules.fonction import GameStrings, Button, Buttongrid, Text, InputBox
from Modules.fonction import verif_size_window, save_game, load_game, create_new_grid, blit_grid
from Modules.fonction import blit_appearance, blit_level_case, create_button_build, play_level
from Modules.fonction import in_case_level, play_world, set_gravity, set_pos_player
from Modules.fonction import verif_level_save, verif_world_save, verif_build_load, get_list_game
from Modules.fonction import get_order_level
from Modules.constant import COLOR, COLOR_TURN, LANG

game_strings = GameStrings(LANG)

# - - - - - main_menu - - - - -

def create_main_menu(window, color, mode):
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

    change_mode_button = Button(window, (0.51, 0.7, 0.14, 0.08),
                          game_strings.get_string(mode), color[1])
    change_mode_button.draw(frame)

    exit_button = Button(window, (0.35, 0.8, 0.3, 0.08),
                         game_strings.get_string('Quit'), color[1])
    exit_button.draw(frame)

    window.blit(frame, (0, 0))
    pygame.display.flip()
    return play_button, build_button, color_button, change_mode_button, exit_button

def main_menu(window, color):
    """
    Affichage du 'main_menu'
    """
    mode = 'level'
    list_button_menu = create_main_menu(window, color, mode)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                proceed = False
                pygame.quit()
            if verif_size_window(window, event):
                list_button_menu = create_main_menu(window, color, mode)
            # Bouton Jouer
            if list_button_menu[0].is_pressed(event):
                proceed = False
                play_world_menu((window, color), 'world1')
                if pygame.get_init():
                    main_menu(window, color)
            # Bouton Build
            elif list_button_menu[1].is_pressed(event):
                proceed = False
                tinker_menu(window, color, mode)
            # Bouton Option
            elif list_button_menu[2].is_pressed(event):
                color = (color[0] + 1, COLOR_TURN[color[0] % 4])
                create_main_menu(window, color, mode)
            # Bouton Autre
            elif list_button_menu[3].is_pressed(event):
                if mode == 'level':
                    mode = 'world'
                else:
                    mode = 'level'
                create_main_menu(window, color, mode)
            # Bouton Quitter
            elif list_button_menu[4].is_pressed(event):
                proceed = False
                pygame.quit()

# - - - - - play_world_menu - - - - -

def create_play_world_menu(display, grid, nbr_level, nbr_coins):
    """
    Mise en place de la logique du 'play_world_menu' avec:
    - 'display' un 2-uples contenant:
        - 'window' la fenêtre
        - 'color' la couleur
    - 'grid' la grille de jeu
    - 'nbr_coins' le nombre de pièce
    - 'nbr_level' le numéro du dernier niveau à faire
    """
    frame = pygame.Surface(display[0].get_size())
    blit_level_case(frame, nbr_level, grid)
    blit_grid(frame, grid)
    blit_appearance(frame, display[1])

    return_button = Button(display[0], (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), display[1][1])
    return_button.draw(frame)

    coin_display = Text(display[0], (0.2, 0.7, 0.08, 0.1), str(nbr_coins) + "x pt")
    coin_display.draw(frame)

    display[0].blit(frame, (0, 0))
    pygame.display.flip()
    return return_button

def play_world_menu(display, name_game, level_order=1, nbr_coins=0):
    """
    Affichage du 'play_world_menu'
    """
    print(level_order)
    grid = load_game(name_game, 'world')
    grid, pos_player = set_pos_player(grid, 'DOWN', 'world')
    return_button = create_play_world_menu(display, grid, level_order, nbr_coins)
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if verif_size_window(display[0], event):
                return_button = create_play_world_menu(display, grid, level_order, nbr_coins)
            elif return_button.is_pressed(event):
                proceed = False
            elif set_gravity(event)[0]:
                direction = set_gravity(event)[1]
                grid, pos_player = play_world(grid, direction, pos_player)
                return_button = create_play_world_menu(display, grid, level_order, nbr_coins)
            elif in_case_level(grid, event, pos_player):
                level_end, add_coins = run_level(display, pos_player, grid, level_order)
                if level_end != -1:
                    proceed = False
                    if pygame.get_init():
                        level_order += level_end
                        nbr_coins += add_coins
                        play_world_menu(display, name_game, level_order, nbr_coins)

# - - - - - play_level_menu - - - - -

def create_play_level_menu(window, color, grid, nbr_coins):
    """
    Mise en place de la logique du 'play_level_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' la grille de jeu
    - 'nbr_coins' le nombre de pièce
    """
    frame = pygame.Surface(window.get_size())
    blit_grid(frame, grid)
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

def play_level_menu(window, color, name_game):
    """
    Affichage du 'play_level_menu'
    """
    grid = load_game(name_game, 'level')
    gravity = 'DOWN'
    grid, pos_player = set_pos_player(grid, gravity, 'level')
    nbr_coins = 0
    lock = False
    finish = False
    proceed = True
    while proceed:
        list_play_level_menu = create_play_level_menu(window, color, grid, nbr_coins)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if verif_size_window(window, event):
                pass
            # Bouton Retour
            elif list_play_level_menu[0].is_pressed(event):
                proceed = False
            # Bouton Reset
            elif list_play_level_menu[1].is_pressed(event):
                grid = load_game(name_game, 'level')
                gravity = 'DOWN'
                grid, pos_player = set_pos_player(grid, gravity, 'level')
                nbr_coins = 0
            if finish:
                proceed = False
                return 1, nbr_coins
            if not lock:
                if set_gravity(event)[0]:
                    gravity = set_gravity(event)[1]
        # var -> (lock, nbr_coins)
        grid, pos_player, finish, var = play_level(grid, gravity, pos_player)
        lock = var[0]
        nbr_coins += var[1]
    return 0, 0

# - - - - - - - Fonction annexe - - - - - - -

def run_level(display, pos_player, grid, level_order):
    """
    Permet de lancer le niveau et de détecter si
    c'est le dernier niveau à jouer avec:
    - 'display' un 2-uples contenant:
        - 'window' la fenêtre
        - 'color' la couleur
    - 'pos_player' la position du joueur
    - 'grid' la grille du menu
    - 'level_order' le numéro du dernier niveau
    """
    # 1
    for level in range(level_order):
        if grid['order'][level] == pos_player:
            name_level = grid[str(pos_player)][0][1]
            level_end, add_coins = play_level_menu(display[0], display[1], name_level)
            # 2
            if level_order - 1 < len(grid['order']):
                if grid['order'][level_order - 1] == pos_player:
                    return level_end, add_coins
            return 0, add_coins
    return -1, 0

# - - - - - tinker_menu - - - - -

def create_tinker_menu(window, color):
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

    create_size_input = InputBox(window, (0.3, 0.25, 0.4, 0.08))

    create_button = Button(window, (0.3, 0.35, 0.4, 0.08),
                           game_strings.get_string('Create'), color[1])
    create_button.draw(frame)

    list_game_button = Button(window, (0.3, 0.55, 0.08, 0.18),
                              "i", color[1])
    list_game_button.draw(frame)

    load_name_input = InputBox(window, (0.4, 0.55, 0.3, 0.08))

    load_button = Button(window, (0.4, 0.65, 0.3, 0.08),
                         game_strings.get_string('Load'), color[1])
    load_button.draw(frame)

    window.blit(frame, (0, 0))
    return (return_button, create_size_input, create_button,
            list_game_button, load_name_input, load_button)

def tinker_menu(window, color, mode):
    """
    Affichage du 'tinker_menu'
    """
    name_load = ''
    list_button_tinker = create_tinker_menu(window, color)
    proceed = True
    grid_size = None
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if verif_size_window(window, event):
                list_button_tinker = create_tinker_menu(window, color)
            # Bouton Retour
            elif list_button_tinker[0].is_pressed(event):
                proceed = False
                main_menu(window, color)
            # Input Taille
            elif list_button_tinker[1].return_pressed(event):
                grid_size = list_button_tinker[1].get_string()
            # Bouton Creer
            elif tm_creation_button((window, color, mode), list_button_tinker[2], grid_size, event):
                proceed = False
            # Bouton Information
            elif list_button_tinker[3].is_pressed(event):
                popup_menu(window, color, 'list_game', mode)
                list_button_tinker = create_tinker_menu(window, color)
            # Input Load
            elif list_button_tinker[4].return_pressed(event):
                name_load = list_button_tinker[4].get_string()
            # Bouton Load
            elif tm_loading_button((window, color, mode), list_button_tinker[5], name_load, event):
                proceed = False
            if proceed:
                # Zone de saisie
                list_button_tinker[1].interact(window, event)
                list_button_tinker[1].draw(window)
                list_button_tinker[4].interact(window, event)
                list_button_tinker[4].draw(window)
                pygame.display.flip()

# - - - - - - - Fonction annexe - - - - - - -

def tm_creation_button(display, button, grid_size, event):
    """
    Fonction annexe de 'tinker_menu'
    Fonction de vérification pour la création de grille avec:
    - 'display' un 3-uples contenant:
        - 'window' la fenêtre
        - 'color' la couleur
        - 'mode' le mode de jeu
    - 'button' le bouton à tester
    - 'size' la taille de la grille
    - 'event' la liste d'évenement pygame
    """
    if button.is_pressed(event):
        try:
            grid_size = int(grid_size)
            if 10 <= grid_size <= 20:
                grid = create_new_grid(grid_size, display[2])
                if display[2] == 'level':
                    build_level_menu(display[0], display[1], grid)
                else:
                    build_world_menu(display[0], display[1], grid)
                return True
            popup_menu(display[0], display[1], 'window_exit', -2)
            create_tinker_menu(display[0], display[1])
        except ValueError:
            popup_menu(display[0], display[1], 'window_exit', -3)
            create_tinker_menu(display[0], display[1])
        except TypeError:
            popup_menu(display[0], display[1], 'window_exit', -3)
            create_tinker_menu(display[0], display[1])
    return False

def tm_loading_button(display, button, name, event):
    """
    Fonction annexe de 'tinker_menu'
    Fonction de vérification pour la sauvegarde de grille avec:
    - 'display' un 3-uples contenant:
        - 'window' la fenêtre
        - 'color' la couleur
        - 'mode' le mode de création (level/world)
    - 'button' le bouton à tester
    - 'name' le nom à chercher
    - 'event' la liste d'évenement pygame
    """
    if button.is_pressed(event):
        if verif_build_load(name, display[2]):
            grid = load_game(name, display[2])
            if display[2] == 'level':
                build_level_menu(display[0], display[1], grid, name)
            else:
                build_world_menu(display[0], display[1], grid, name)
            return True
        popup_menu(display[0], display[1], 'window_exit', -1)
        create_tinker_menu(display[0], display[1])
    return False

# - - - - - build_menu - - - - -

# - - - - - - - level - - - - - - -

def create_build_level_menu(window, color, grid, name_save):
    """
    Mise en place de la logique du 'build_level_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' la grille de jeu
    - 'name_save' le nom de sauvegarde
    """
    frame = pygame.Surface(window.get_size())

    # Zone de détection du tableau
    grid_button = Buttongrid(window, grid)

    # Affiche la grille de jeu
    blit_grid(frame, grid)

    # Bordure du niveau
    blit_appearance(frame, color, grid)

    # Bouton des blocs
    button_block = create_button_build(frame, 'level')
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

    save_name_input = InputBox(window, (0.85, 0.15, 0.1, 0.08), name_save)

    window.blit(frame, (0, 0))

    return return_button, save_button, grid_button, button_block, test_button, save_name_input

def build_level_menu(window, color, grid, name_save=''):
    """
    Affichage du 'build_level_menu'
    """
    list_button_build_l = create_build_level_menu(window, color, grid, name_save)
    rajout_case = 0
    display = (window, color, 'level')
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if verif_size_window(window, event):
                list_button_build_l = create_build_level_menu(window, color, grid, name_save)
            # Bouton Retour
            elif list_button_build_l[0].is_pressed(event):
                proceed = False
                tinker_menu(window, color, 'level')
            # Bouton Test
            elif bl_saving_menu(display, list_button_build_l[4], (grid, name_save), event):
                proceed = False
                play_level_menu(window, color, name_save)
                if pygame.get_init():
                    build_level_menu(window, color, grid, name_save)
            # Zone de saisie entré
            elif list_button_build_l[5].return_pressed(event):
                name_save = list_button_build_l[5].get_string()
            if proceed:
                # Bouton Sauvegarde
                bl_saving_menu(display, list_button_build_l[1], (grid, name_save), event)
                # Changement de case
                game = (grid, name_save, rajout_case)
                bl_change_box(display, list_button_build_l[2], game, event)
                # Button créateur
                list_button_touch = list_button_build_l[3]
                for place in list_button_touch:
                    if list_button_touch[place].is_pressed(event):
                        rajout_case = place
                # Zone de saisie
                list_button_build_l[5].interact(window, event)
                list_button_build_l[5].draw(window)
                pygame.display.flip()

# - - - - - - - world - - - - - - -

def create_build_world_menu(window, color, grid, name_save):
    """
    Mise en place de la logique du 'build_world_menu' avec:
    - 'window' la fenêtre
    - 'color' la couleur
    - 'grid' la grille de jeu
    - 'name_save' le nom de sauvegarde
    """
    frame = pygame.Surface(window.get_size())

    # Zone de détection du tableau
    grid_button = Buttongrid(window, grid)

    # Affiche la grille de jeu
    blit_grid(frame, grid)
    blit_level_case(frame, 0, grid, 'edit')

    # Bordure du niveau
    blit_appearance(frame, color, grid)

    # Bouton des blocs
    button_block = create_button_build(frame, 'world')
    # Bouton retour
    return_button = Button(window, (0.05, 0.05, 0.1, 0.08),
                           game_strings.get_string('Return'), color[1])
    return_button.draw(frame)
    # Bouton sauvegarde
    save_button = Button(window, (0.85, 0.05, 0.1, 0.08),
                         game_strings.get_string('Save'), color[1])
    save_button.draw(frame)

    save_name_input = InputBox(window, (0.85, 0.15, 0.1, 0.08), name_save)

    list_level_button = Button(window, (0.85, 0.37, 0.1, 0.18),
                               "i", color[1])
    list_level_button.draw(frame)

    load_name_input = InputBox(window, (0.85, 0.57, 0.1, 0.08))

    window.blit(frame, (0, 0))

    return (return_button, save_button, grid_button, button_block, save_name_input,
            list_level_button, load_name_input)

def build_world_menu(window, color, grid, name_save=''):
    """
    Affichage du 'build_world_menu'
    """
    list_button_build_w = create_build_world_menu(window, color, grid, name_save)
    rajout_case = 0
    name_level_load = ''
    display = (window, color, 'world')
    proceed = True
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if verif_size_window(window, event):
                list_button_build_w = create_build_world_menu(window, color, grid, name_save)
            # Bouton Retour
            elif list_button_build_w[0].is_pressed(event):
                proceed = False
                tinker_menu(window, color, 'world')
            # Zone de saisie entré
            elif list_button_build_w[4].return_pressed(event):
                name_save = list_button_build_w[4].get_string()
            # Bouton Information
            elif list_button_build_w[5].is_pressed(event):
                popup_menu(window, color, 'list_game', 'level')
                list_button_build_w = create_build_world_menu(window, color, grid, name_save)
            # Input Load
            elif list_button_build_w[6].return_pressed(event):
                name_level_load = list_button_build_w[6].get_string()
            if proceed:
                # Bouton Sauvegarde
                bl_saving_menu(display, list_button_build_w[1], (grid, name_save), event)
                # Changement de case
                game = (grid, name_save, rajout_case, name_level_load)
                bl_change_box(display, list_button_build_w[2], game, event)
                # Button créateur
                list_button_touch = list_button_build_w[3]
                for place in list_button_touch:
                    if list_button_touch[place].is_pressed(event):
                        rajout_case = place
                # Zone de saisie
                list_button_build_w[4].interact(window, event)
                list_button_build_w[4].draw(window)
                list_button_build_w[6].interact(window, event)
                list_button_build_w[6].draw(window)
                pygame.display.flip()

# - - - - - - - Fonction annexe - - - - - - -

def bl_change_box(display, button, game, event):
    """
    Fonction annexe des 'build_menu'
    Permet de changer l'objet dans la casse cliqué avec:
    - 'display' un 3-uples avec:
        - 'window' la fenêtre
        - 'color' la couleur
        - 'mode' le mode de création (level/world)
    - 'button' le bouton cliqué
    - 'game' un 5-uples avec:
        - 'grid' la grille de jeu
        - 'name_grid' le nom de la grille
        - 'new_case' l'objet à rajouté dans la case
        - 'name_level' le nom du niveau quand c'est une case niveau à placer
    """
    if button.is_pressed(event):
        coord = button.get_coord()
        if game[0][str(coord)][0][0] == 0:
            if game[2] == -2:
                if game[3] != '':
                    if verif_build_load(game[3], 'level'):
                        game[0][str(coord)] = ((game[2], game[3]), game[0][str(coord)][1])
                    else:
                        popup_menu(display[0], display[1], 'window_exit', -1)
                else:
                    popup_menu(display[0], display[1], 'window_exit', 6)
            else:
                game[0][str(coord)] = ((game[2], None), game[0][str(coord)][1])
        else:
            game[0][str(coord)] = ((0, None), game[0][str(coord)][1])
        if display[2] == 'level':
            create_build_level_menu(display[0], display[1], game[0], game[1])
        else:
            game[0]['order'] = get_order_level(coord, game[0]['order'], game[0])
            create_build_world_menu(display[0], display[1], game[0], game[1])

def bl_saving_menu(display, button, game, event):
    """
    Fonction annexe des 'build_menu'
    Fonction de vérification pour la sauvegarde de la grille avec:
    - 'display' un 3-uples contenant:
        - 'window' la fenêtre
        - 'color' la couleur
        - 'mode' le mode de création (level/world)
    - 'button' le bouton à tester
    - 'game' un 2-uples contenant:
        - 'grid' la grille
        - 'grid_name' le nom de la grille
    - 'event' la liste d'évenement pygame
    """
    if button.is_pressed(event):
        if display[2] == 'level':
            exit_code = verif_level_save(game[0], game[1])
        else:
            exit_code = verif_world_save(game[0], game[1])
        popup_menu(display[0], display[1], 'window_exit', exit_code)
        if exit_code in ('0w', '0l'):
            save_game(game[1], display[2], game[0])
            if display[2] == 'level':
                create_build_level_menu(display[0], display[1], game[0], game[1])
            else:
                create_build_world_menu(display[0], display[1], game[0], game[1])
            return True
        if display[2] == 'level':
            create_build_level_menu(display[0], display[1], game[0], game[1])
        else:
            create_build_world_menu(display[0], display[1], game[0], game[1])
    return False

# - - - - - popup_menu - - - - -

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

def create_list_game_menu(window, color, mode):
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

    list_game = get_list_game(mode)
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
        - 'mode' pour la fenêtre 'list_game'
        - 'exit_code' pour la fenêtre 'window_exit'
    """
    proceed = True
    while proceed:
        if name_menu == "list_game":
            create_list_game_menu(window, color, other)
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
