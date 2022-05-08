"""
Ce module s'occupe des différentes fonction nécessaire au bon fonctionnement du jeu
"""
import json
import os
from math import sqrt
import pygame
from Modules.constant import COLOR, FONT_HEIGHT, TEXTURE


def get_font_size(font_height):
    """
    récupère une valeur de taille de police selon `font_height` un entier
    représentant la hauteur de font voulu en nombre de pixel sur la fenêtre
    """
    if font_height < 19:
        return 12
    else:
        i = 0
        try:
            while font_height > FONT_HEIGHT[i]:
                i += 1
        except IndexError:
            pass
        return i + 12

def verif_size_window(window, event):
    """
    Permet de vérifier si 'window' n'est pas trop petit
    """
    if event.type == pygame.VIDEORESIZE:
        window_w, window_h = window.get_size()
        if window_w < 500 or window_h < 250:
            window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
        return True
    return False

def save_game(name, folder, grid):
    """
    Permet de sauvegarder 'grid' de forme dico en format json
    dans l'emplacement 'Others/Create_game/Save_level/'name'.json',
    avec'name' le dossier d'arriver
    """
    filename = "Others/Create_game/Save_" + folder + "/" + name + ".json"

    with open(filename, "w") as file:
        json.dump(grid, file)
    file.close()

def load_game(name, folder):
    """
    Permet de charger le dico stocker en format json
    de la grille 'name' dans l'emplacement
    'Others/Create_game/Save_level/'name'.json'
    """
    filename = "Others/Create_game/Save_" + folder + "/" + name + ".json"

    with open(filename) as file:
        dict_grid = json.load(file)
    file.close()
    return dict_grid

def get_list_game(mode):
    """
    Permet d'obtenir la liste des sauvegardes
    dans l'emplacement 'Others/Create_game/Save_level/'
    """
    list_game = os.listdir('Others/Create_game/Save_' + mode + '/')
    return list_game

def create_new_grid(dimension, mode):
    """
    Permet de générer un dico avec pour clé le numéro de la case
    allant de 1 à dimension^2 sous forme str
    Les valeurs de chaque clé correspondent à :
        (('id de l'objet', 'info de l'objet'*), 'gravité du joueur'*)
        avec * = None si non spécifié
    """
    grid = {}
    for box in range(dimension ** 2):
        grid[str(box)] = ((0, None), None)
    if mode == 'world':
        grid['order'] = []
    return grid

def get_dimension_grid(window):
    """
    Permet de déterminer le côté le plus petit
    pour afficher la grille de jeu
    """
    window_w, window_h = window.get_size()
    x_value = window_w * 0.6
    y_value = window_h * 0.7
    if x_value < y_value:
        return x_value
    return y_value

def blit_grid(frame, grid):
    """
    Permet d'afficher la grille avec les objets
    avec comme argument :
    - 'frame' la fenêtre sur laquel afficher la grille
    - 'grid' la grille de jeu
    """
    dimension_grid = get_dimension_grid(frame)
    grid_size = int(sqrt(len(grid)))
    scale = int(dimension_grid / grid_size) + 1
    window_w = (frame.get_size())[0]
    for box in grid:
        if box != 'order':
            coordonne_box = int(box) // grid_size, int(box) % grid_size
            x_coord = (window_w - dimension_grid) / 2
            x_value = int(x_coord + (dimension_grid / grid_size) * coordonne_box[1])
            y_value = int((dimension_grid / grid_size) * coordonne_box[0])
            if grid[box][0][0] not in (-2, 0):
                image = pygame.transform.scale(TEXTURE[grid[box][0][0]], (scale, scale))
                frame.blit(image, (x_value + 1, y_value + 1))
            if grid[box][1] is not None:
                image_player = pygame.transform.scale(TEXTURE[grid[box][1]], (scale, scale))
                frame.blit(image_player, (x_value + 1, y_value + 1))
    return frame

def blit_level_case(frame, nbr_level, grid, mode=''):
    """
    Permet d'afficher les niveaux avec la couleur correspondante avec:
    - 'frame' la fenêtre sur laquel afficher la grille
    - 'nbr_level' le numéro du dernier niveau à faire
    - 'grid' la grille de jeu
    """
    dimension_grid = get_dimension_grid(frame)
    grid_size = int(sqrt(len(grid)))
    scale = int(dimension_grid / grid_size) + 1
    window_w = (frame.get_size())[0]
    for level in range(len(grid['order'])):
        coord_box = int(grid['order'][level]) // grid_size, int(grid['order'][level]) % grid_size
        x_coord = (window_w - dimension_grid) / 2
        x_value = int(x_coord + (dimension_grid / grid_size) * coord_box[1])
        y_value = int((dimension_grid / grid_size) * coord_box[0])
        if nbr_level - 1 == level or mode == 'edit':
            level_texture = -2
        elif nbr_level -1 < level:
            level_texture = -1
        else:
            level_texture = 0
        image = pygame.transform.scale(TEXTURE[level_texture], (scale, scale))
        frame.blit(image, (x_value + 1, y_value + 1))
    return frame

def blit_appearance(surface, color, grid=''):
    """
    Permet d'afficher l'affichage utilisé pour différente raison
    """
    window_w = (surface.get_size())[0]
    dimension_grid = get_dimension_grid(surface)
    start_grid = (window_w - dimension_grid) // 2
    if grid != '':
        grid_size = int(sqrt(len(grid)))
        box_size = dimension_grid / grid_size
        for x_value in range(1, grid_size):
            for y_value in range(1, grid_size):
                corner = pygame.Rect(start_grid + box_size * x_value, box_size * y_value, 2, 2)
                pygame.draw.rect(surface, COLOR['WHITE'], corner)
    outline = pygame.Rect(start_grid, 0, dimension_grid + 1, dimension_grid + 1)
    pygame.draw.rect(surface, COLOR['GRAY'], outline, 1)
    line_1 = Line(surface, (0, 0.7, 1, 0.7), color[1])
    line_1.draw(surface)
    line_2 = Line(surface, (0.2, 0, 0.2, 0.7), color[1])
    line_2.draw(surface)
    line_3 = Line(surface, (0.8, 0, 0.8, 0.7), color[1])
    line_3.draw(surface)

def create_button_build(surface, mode):
    """
    Permet d'afficher le boutons permettant de choisir
    ce que l'on souhaite placer dans la grille
    """
    if mode == 'level':
        place = 1
        end_place = 9
    else:
        place =  -4
        end_place = -2
    button_return = {}
    for i in range(3):
        y_value = 0.735 + ((0.045 + 0.04) * i)
        for j in range(15):
            x_value = 0.025 + ((0.025 + 0.04) * j)
            button = Buttonimage(surface, (x_value, y_value, 0.04), TEXTURE[place])
            button.draw(surface)
            button_return[place] = button
            place += 1
            if place >= end_place + 1:
                return button_return
    return None

def play_world(grid, direction, pos_player):
    """
    Permet de jouer avec le personnage dans le monde
    """
    limit, new_pos = shift_player(grid, pos_player, direction)
    if not limit:
        if grid[str(new_pos)][0][0] != 0:
            grid[str(pos_player)][1] = None
            grid[str(new_pos)][1] = 'DOWN'
            pos_player = new_pos
    return grid, pos_player

def in_case_level(grid, event, pos_player):
    """
    Permet de savoir si le joueur se trouve sur une case niveau
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if grid[str(pos_player)][0][0] == -2:
                return True
    return False

def get_order_level(coord_modif, order, grid):
    """
    Permet d'avoir l'ordre d'accomplissement des niveaux avec:
        - 'coord_modif' la case qui à subit une modification
        - 'order' l'ordre des niveaux actuel
        - 'grid' la grille de jeu
    """
    level_enter_count = 0
    for case in grid:
        if case != 'order':
            if grid[case][0][0] == -2:
                level_enter_count += 1
    if len(order) < level_enter_count:
        order.append(coord_modif)
    if len(order) > level_enter_count:
        new_order = []
        for case in order:
            if case != coord_modif:
                new_order.append(case)
        return new_order
    return order

def play_level(grid, gravity, pos_player):
    """
    Permet de jouer avec le personnage dans le niveau
    """
    coin = 0
    limit, new_pos = shift_player(grid, pos_player, gravity)
    if not limit:
        if grid[str(new_pos)][0][0] != 3:
            # Pour les pièces
            grid, coin = get_coin(grid, new_pos)
            grid[str(pos_player)][1] = None
            grid[str(new_pos)][1] = gravity
            pos_player = new_pos
            lock = True
        else:
            lock = False
    else:
        lock = False
    # Sortie atteinte
    finish = get_finish(grid, pos_player)
    return grid, pos_player, finish, (lock, coin)

def get_finish(grid, pos_player):
    """
    Permet de détecter si le joueur est arrivé à la fin
    """
    if grid[str(pos_player)][0][0] == 2:
        return True
    return False

def get_coin(grid, new_pos):
    """
    Permet la récupération des pièces
    """
    coin = 0
    if grid[str(new_pos)][0][0] == 8:
        coin = 1
        grid[str(new_pos)][0][0] = 0
    return grid, coin

def shift_player(grid, pos_player, direction):
    """
    Permet de déplacer le joueur dans la grille en vérifiant
    si le joueur ne se trouve pas au bord de cette grille avec:
    - 'grid' correspond à la grille
    - 'pos_player' la position initiale du joueur
    - 'gravity' la gravité à laquelle le joueur est soumis
    """
    dimension_grid = int(sqrt(len(grid)))
    if direction == "DOWN":
        if not pos_player + dimension_grid > len(grid) - 1:
            return False, pos_player + dimension_grid
    elif direction == "RIGHT":
        if not (pos_player + 1) % dimension_grid == 0:
            return False, pos_player + 1
    elif direction == "UP":
        if not pos_player - dimension_grid < 0:
            return False, pos_player - dimension_grid
    elif direction == "LEFT":
        if not (pos_player - 1) % dimension_grid == dimension_grid - 1:
            return False, pos_player - 1
    return True, None

def set_pos_player(grid, gravity, mode):
    """
    Remplace la zone d'apparition par le joueur et
    renvoie son emplacement lors de l'initialisation
    """
    place = None
    if mode == 'level':
        start = 1
    else:
        start = -4
    for value in grid:
        if value != 'order':
            if grid[value][0][0] == start:
                place = int(value)
                grid[value][1] = gravity
    return grid, place

def set_gravity(event):
    """
    Renvoie la gravité par rapport à la flèche choisit
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            return True, 'UP'
        if event.key == pygame.K_RIGHT:
            return True, 'RIGHT'
        if event.key == pygame.K_DOWN:
            return True, 'DOWN'
        if event.key == pygame.K_LEFT:
            return True, 'LEFT'
    return False, None

def verif_level_save(grid, name_save):
    """
    Permet de voir si il n'y a pas
    d'erreur pour sauvegarder le niveau
    """
    count_enter = 0
    for case in grid:
        if grid[case][0][0] == 1:
            count_enter += 1
    # Pas d'entrée
    if count_enter < 1:
        return 1
    # Trop d'entrée
    if count_enter > 1:
        return 2
    # Nom non complété
    if len(name_save) == 0:
        return 3
    # Nom trop court
    if len(name_save) < 3:
        return 4
    # Tout est bon
    return '0l'

def verif_world_save(grid, name_save):
    """
    Permet de voir si il n'y a pas
    d'erreur pour sauvegarder le niveau
    """
    count_enter = 0
    count_level = 0
    for case in grid:
        if case != 'order':
            if grid[case][0][0] == -4:
                count_enter += 1
            if grid[case][0][0] == -2:
                count_level += 1
    # Pas d'entrée
    if count_enter < 1:
        return 1
    # Trop d'entrée
    if count_enter > 1:
        return 2
    if len(name_save) == 0:
        return 3
    # Nom trop court
    if len(name_save) < 3:
        return 4
    # Pas de niveau
    if count_level == 0:
        return 5
    # Tout est bon
    return '0w'

def verif_build_load(name_load, mode):
    """
    Permet de vérifier si 'name_load' répond aux attentes
    """
    if name_load + ".json" in get_list_game(mode):
        return True
    return False

class GameStrings:
    """
    Classe permettant de gérer les chaines de caractères du jeu.
    """
    def __init__(self, language="Fr"):
        with open(
            f"./Others/Game_string/{language}/game_string.json",
            "r", encoding="utf-8"
        ) as fichier:
            self.data = json.load(fichier)

    def get_string(self, key):
        """
        Permet de récupérer une chaine de caractères à partir de sa clé.
        """
        return self.data[key]

    def get_all_strings(self):
        """
        Permet de récupérer toutes les chaines de caractères.
        """
        return self.data


class Button:
    """
    crée un bouton visuel avec un texte centré
    """
    def __init__(self, window, relative_position, text, color):
        """
        Initialise le bouton avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'relative_position' un 4-uple (x, y, w, h)
            - 'x' la position x par rapport à la largeur de la fenêtre
                0 -> à gauche / 1 -> à droite (sortit de fenêtre)
            - 'y' la position y par rapport à la hauteur de la fenêtre
                0 -> en haut / 1 -> en bas (sortit de fenêtre)
            - 'w' correspond à la largeur du bouton par rapport à la
                largeur de la fenêtre
                0 -> bouton inexistant / 1 -> largeur de la fenêtre
            - 'h' correspond à la hauteur du bouton par rapport à la
                hauteur de la fenêtre
                0 -> bouton inexistant / 1 -> hauteur de la fenêtre
        - 'text' correspond au texte qui doit être affiché sur le bouton
            doit être sous forme d'une chaîne de caractère
        - 'color' correspond à la couleur des boutons, la version original
            pour les bords et la version sombre pour les fonds
        """
        self.relative_position = relative_position
        self.text = text
        self.color = color
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton par rapport à la dimension
        de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        x_value = round(self.relative_position[0] * window_w)
        y_value = round(self.relative_position[1] * window_h)
        w_value = round(self.relative_position[2] * window_w)
        h_value = round(self.relative_position[3] * window_h)
        self.rect = pygame.Rect(x_value, y_value, w_value, h_value)
        font_size = get_font_size(round(self.rect.h * 0.6))
        font = pygame.font.SysFont("Impact", font_size)
        self.text_image = font.render(self.text, 1, COLOR['WHITE'])
        self.text_pos = self.text_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Permet d'afficher le bouton sur la surface 'surface'
        """
        pygame.draw.rect(surface, COLOR["DARK_" + self.color], self.rect)
        pygame.draw.rect(surface, COLOR[self.color], self.rect, 3)
        surface.blit(self.text_image, self.text_pos)

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


class Buttongrid:
    """
    Crée un bouton invisible de la taille de la grille
    """
    def __init__(self, window, grid):
        """
        Initialise le bouton avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'dimension_grid' qui correspond à la longueur du côté du
            quadrillage
        - 'grid' qui correspond à la grille
        """
        self.dimension_grid = get_dimension_grid(window)
        self.grid_size = int(sqrt(len(grid)))
        self.mouse = pygame.mouse.get_pos()
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton
        """
        window_w = (window.get_size())[0]
        self.x_value = (window_w - self.dimension_grid) // 2
        y_value = 0
        w_value = self.dimension_grid
        h_value = self.dimension_grid
        self.rect = pygame.Rect(self.x_value, y_value,
                                w_value, h_value)

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.mouse = pygame.mouse.get_pos()
                    return True
        return False

    def get_coord(self):
        """
        Permet de récuperer le numéro de la case cliqué
        """
        box_dimension = self.dimension_grid / self.grid_size
        coord_x = ((self.mouse[0] - self.x_value) / box_dimension)
        if coord_x > self.grid_size - 1:
            coord_x = self.grid_size - 1
        coord_y = self.mouse[1] // box_dimension
        if coord_y > self.grid_size - 1:
            coord_y = self.grid_size - 1
        return int(coord_x + coord_y * self.grid_size)


class Buttonimage:
    """
    Permet de créer un bouton de forme carré avec une image
    """
    def __init__(self, window, relative_position, image, color='DARK_GRAY'):
        """Initialise le bouton avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'relative_position' un 3-uple (x, y, w)
            - 'x' la position x par rapport à la largeur de la fenêtre
                0 -> à gauche / 1 -> à droite (sortit de fenêtre)
            - 'y' la position y par rapport à la hauteur de la fenêtre
                0 -> en haut / 1 -> en bas (sortit de fenêtre)
            - 'w' correspond à la longueur du côté du bouton par rapport
                à la largeur ou à la hauteur de la fenêtre
                (au plus petit des deux)
        """
        self.relative_position = relative_position
        self.image = image
        self.color = COLOR[color]
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton carré et l'image
        par rapport au dimension de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        self.x_value = round(self.relative_position[0] * window_w)
        self.y_value = round(self.relative_position[1] * window_h)
        self.w_value = round(self.relative_position[2] * window_w)
        self.rect = pygame.Rect(self.x_value, self.y_value,
                                self.w_value, self.w_value)
        scale = self.w_value
        self.image = pygame.transform.scale(self.image, (scale, scale))

    def draw(self, surface):
        """
        Permet d'afficher le bouton carré avec l'image
        """
        surface.blit(self.image, (self.x_value, self.y_value))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


class Text:
    """
    crée un texte centré
    """
    def __init__(self, window, relative_position, text):
        """
        Initialise le bouton avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'relative_position' un 4-uple (x, y, w, h)
            - 'x' la position x par rapport à la largeur de la fenêtre
                0 -> à gauche / 1 -> à droite (sortit de fenêtre)
            - 'y' la position y par rapport à la hauteur de la fenêtre
                0 -> en haut / 1 -> en bas (sortit de fenêtre)
            - 'w' correspond à la largeur du texte par rapport à la
                largeur de la fenêtre
                0 -> texte inexistant / 1 -> largeur de la fenêtre
            - 'h' correspond à la hauteur du texte par rapport à la
                hauteur de la fenêtre
                0 -> texte inexistant / 1 -> hauteur de la fenêtre
        - 'text' correspond au texte qui doit être affiché, il
            doit être sous forme d'une chaîne de caractère
        """
        self.relative_position = relative_position
        self.text = str(text)
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le texte par rapport à la dimension
        de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        x_value = round(self.relative_position[0] * window_w)
        y_value = round(self.relative_position[1] * window_h)
        w_value = round(self.relative_position[2] * window_w)
        h_value = round(self.relative_position[3] * window_h)
        self.rect = pygame.Rect(x_value, y_value,
                                w_value, h_value)
        font_size = get_font_size(round(self.rect.h * 0.6))
        font = pygame.font.SysFont("Impact", font_size)
        self.text_image = font.render(self.text, 1, COLOR['WHITE'])
        self.text_pos = self.text_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Permet d'afficher le texte sur la surface 'surface'
        """
        surface.blit(self.text_image, self.text_pos)


class InputBox:
    """
    Crée une zone d'insertion de texte
    """
    def __init__(self, window, relative_position, text=''):
        """
        Initialise la zone d'insertion avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'relative_position' un 4-uple (x, y, w, h)
            - 'x' la position x par rapport à la largeur de la fenêtre
                0 -> à gauche / 1 -> à droite (sortit de fenêtre)
            - 'y' la position y par rapport à la hauteur de la fenêtre
                0 -> en haut / 1 -> en bas (sortit de fenêtre)
            - 'w' correspond à la largeur de la zone par rapport à la
                largeur de la fenêtre
                0 -> texte inexistant / 1 -> largeur de la fenêtre
            - 'h' correspond à la hauteur de la zone par rapport à la
                hauteur de la fenêtre
                0 -> texte inexistant / 1 -> hauteur de la fenêtre
        - 'other' un 2-uple contenant:
            - 'text' le texte avec lequel il travaille
            - 'max_len' la longueur maximale de la chaîne de caractère
        """
        self.relative_position = relative_position
        self.text = text
        self.active = False
        self.text_surface = ''
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton par rapport à la dimension
        de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        x_value = round(self.relative_position[0] * window_w)
        y_value = round(self.relative_position[1] * window_h)
        w_value = round(self.relative_position[2] * window_w)
        h_value = round(self.relative_position[3] * window_h)
        self.rect = pygame.Rect(x_value, y_value,
                                w_value, h_value)
        font_size = get_font_size(round(self.rect.h * 0.6))
        self.font = pygame.font.SysFont("Impact", font_size)
        self.text_surface = self.font.render(self.text, 1, COLOR['WHITE'])
        self.text_pos = self.text_surface.get_rect(center=self.rect.center)

    def interact(self, window, event):
        """
        Permet d'intéragir avec la zone de saisie, aussi bien
        pour la sélectionner que pour écrire
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) <= 9 and not event.key == pygame.K_RETURN:
                    self.text += event.unicode
                self.resize(window)
            self.text_surface = self.font.render(self.text, True, COLOR['WHITE'])

    def return_pressed(self, event):
        """
        Renvoie 'True' si la touche Return est pressé,
        sinon renvoie 'False'
        """
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
        return False

    def get_string(self):
        """
        Permet de récupérer le texte qui y est écrit en chaîne de caractère
        """
        return str(self.text)

    def draw(self, screen):
        """
        Permet d'afficher la zone de saisie sur la fenêtre 'screen'
        """
        pygame.draw.rect(screen, COLOR['BLACK'], self.rect)
        screen.blit(self.text_surface, self.text_pos)
        pygame.draw.rect(screen, COLOR['GRAY'], self.rect, 2)


class Line:
    """
    Créer un ligne
    """
    def __init__(self, window, relative_position, color):
        """
        Initialise une ligne avec comme argument:
        - 'window' qui correspond à la fenêtre sur lequel la ligne s'affiche
        - 'relative_position' un 4-uple (x, y, w, h):
            - 'x' la position de départ par rapport à la largeur de la fenêtre
            - 'y' la position de départ par rapport à la hauteur de la fenêtre
            - 'w' la position d'arrivée par rapport à la largeur de la fenêtre
            - 'h' la position d'arrivée par rapport à la hauteur de la fenêtre
        - 'color' la clé de la couleur du dico COLOR
        """
        self.relative_position = relative_position
        self.color = COLOR['DARK_' + color]
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner et de placer la ligne par rapport à la fenêtre
        'window'
        """
        window_w, window_h = window.get_size()
        x_value = round(self.relative_position[0] * window_w)
        y_value = round(self.relative_position[1] * window_h)
        w_value = round(self.relative_position[2] * window_w)
        h_value = round(self.relative_position[3] * window_h)
        self.rect_start = x_value, y_value
        self.rect_finish = w_value, h_value

    def draw(self, surface):
        """
        Permet d'afficher la ligne sur la surface 'surface'
        """
        pygame.draw.line(surface, self.color,
                         self.rect_start, self.rect_finish, 3)
