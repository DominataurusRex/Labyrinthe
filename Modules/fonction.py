from email.errors import NoBoundaryInMultipartDefect
import pygame
import json
from Modules.constant import COLOR, FONT_HEIGHT

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

def write_game(name, grid):
    """
    Permet de sauvegarder 'grid' de forme dico en format json
    dans l'emplacement 'Others/Game_save/'name'.json,
    avec'name' le dossier d'arriver
    """
    fileName = "Others/Game_save/" + name + ".json"

    with open(fileName, "w") as file:
        json.dump(grid, file)
    file.close()

def create_new_grid(dimension):
    """
    Permet de générer un dico avec pour clé les coordonnées
    x et y séparer d'un '-', sous la forme str
    """
    grid = {}
    for box in range(dimension ** 2):
        grid[str(box)] = 0
    return grid


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
        self.color_ext = COLOR[color]
        self.color_int = COLOR['DARK_' + color]
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton par rapport à la dimension
        de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        self.x_value = round(self.relative_position[0] * window_w)
        self.y_value = round(self.relative_position[1] * window_h)
        self.w_value = round(self.relative_position[2] * window_w)
        self.h_value = round(self.relative_position[3] * window_h)
        self.rect = pygame.Rect(self.x_value, self.y_value, self.w_value, self.h_value)
        font_size = get_font_size(round(self.rect.h * 0.6))
        font = pygame.font.SysFont("Impact", font_size)
        self.text_image = font.render(self.text, 1, COLOR['WHITE'])
        self.text_pos = self.text_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Permet d'afficher le bouton sur la surface 'surface'
        """
        pygame.draw.rect(surface, self.color_int, self.rect)
        pygame.draw.rect(surface, self.color_ext, self.rect, 3)
        surface.blit(self.text_image, self.text_pos)

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        dimension_x = self.x_value + self.w_value
        dimension_y = self.y_value + self.h_value
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse = pygame.mouse.get_pos()
                if self.x_value <= mouse[0] <= dimension_x and self.y_value <= mouse[1] <= dimension_y:
                    return True
        return False

class Button_grid:
    """
    crée un bouton invisible
    """
    def __init__(self, window, dimension_grid, grid_size):
        """
        Initialise le bouton avec comme argument:
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'dimension_grid' qui correspond à la longueur du côté du
            quadrillage
        - 'grid_size' qui correspond au nombre de case qu'il y a par côté
        """
        self.dimension_grid = dimension_grid
        self.grid_size = grid_size
        self.resize(window)

    def resize(self, window):
        """
        Permet de redimensionner le bouton
        """
        window_w, window_h = window.get_size()
        self.x_value = (window_w - self.dimension_grid) // 2
        self.y_value = 0
        self.w_value = self.dimension_grid
        self.h_value = self.dimension_grid

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        dimension_x = self.x_value + self.w_value
        dimension_y = self.y_value + self.h_value
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse = pygame.mouse.get_pos()
                if self.x_value <= self.mouse[0] <= dimension_x and self.y_value <= self.mouse[1] <= dimension_y:
                    return True
        return False
    
    def get_coord(self):
        """
        Permet de récuperer le numéro de la case cliqué
        """
        box_dimension = self.dimension_grid // self.grid_size
        coord_x = ((self.mouse[0] - self.x_value) // box_dimension)
        if coord_x > self.grid_size - 1:
            coord_x = self.grid_size - 1
        coord_y = self.mouse[1] // box_dimension
        if coord_y > self.grid_size - 1:
            coord_y = self.grid_size - 1
        return int(coord_x + coord_y * self.grid_size)

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
        Permet de redimensionner le bouton par rapport à la dimension
        de la fenêtre 'window'
        """
        window_w, window_h = window.get_size()
        self.x_value = round(self.relative_position[0] * window_w)
        self.y_value = round(self.relative_position[1] * window_h)
        self.w_value = round(self.relative_position[2] * window_w)
        self.h_value = round(self.relative_position[3] * window_h)
        self.rect = pygame.Rect(self.x_value, self.y_value, self.w_value, self.h_value)
        font_size = get_font_size(round(self.rect.h * 0.6))
        font = pygame.font.SysFont("Impact", font_size)
        self.text_image = font.render(self.text, 1, COLOR['WHITE'])
        self.text_pos = self.text_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Permet d'afficher le texte sur la surface 'surface'
        """
        surface.blit(self.text_image, self.text_pos)



class Fence:
    """
    Génère un quadrillage centré horizontalement et en haut de la fenêtre
    dans une zone précise
    """
    def __init__(self, window, nbr_box):
        """
        Initialise un quadrillage de forme carré avec comme argument
        - 'window' qui correspond à la fenêtre sur laquel il va se générer
        - 'nbr_box' qui correspond aux nombres de case que le quadrillage
            doit comporter sur un côté
        """
        self.nbr_box = nbr_box
        self.resize(window)
    
    def resize(self, window):
        """
        - Permet de centré la quadrillage carré au milieu de la longueur en haut
            quelque soit le nombre de case
        - Le carré doit apparaitre dans une zone défini de la fenêtre
            dans (0.2, 0, 0.8, 0.8), ce qui fait par conséquence varié la
            longueur du côté et l'emplacement du quadrillage
        """
        window_w, window_h = window.get_size()
        # Permet de déterminer le côté le plus petit pour la quadrillage
        if window_w * 0.6 < window_h * 0.8:
            self.dimension_grid = (window_w * 0.6) // 1
        else:
            self.dimension_grid = (window_h * 0.8) // 1
        # Permet de savoir le côté des cases du quadrillage
        self.dimension_box = self.dimension_grid // self.nbr_box
        # Permet de savoir l'abscisse d'origine du quadrillage
        self.x_value = ((window_w - self.dimension_grid) // 2)
    
    def draw(self, frame):
        """
        Permet d'afficher le quadrillage en dessinant chaque case
        """
        for lenght in range(self.nbr_box):
            # Modifie la valeur de x des cases
            y_value = 0
            for height in range(self.nbr_box):
                # Modifie la valeur de y pour les cases
                self.rect = pygame.Rect(self.x_value, y_value, self.dimension_box, self.dimension_box)
                pygame.draw.rect(frame,COLOR['GRAY'], self.rect, 1)
                y_value += self.dimension_box
            self.x_value += self.dimension_box
    
    def get_dimension_grid(self):
        """
        Permet de récupérer la dimension du quadrillage
        """
        return self.dimension_grid
    

class Grid:
    """
    Créer un niveau
    """
    def __init__(self, window, grid, dimension_grid, grid_size):
        """
        Initialise un niveau avec comme argument:
        - 'window' qui correspond à la fenêtre sur lequel le
            niveau s'affiche
        - 'grid' le dictionnaire qui correspond au niveau
        - 'dimension_grid' qui corrspond à la taille du tableau
            au final
        - 'grid_size' qui correspond au nombre de case de côté
        """
        self.window = window
        self.grid = grid
        self.dimension_grid = dimension_grid
        self.grid_size = grid_size
        self.resize(window)
    
    def resize(self, window):
        window_w, window_h = window.get_size()
        self.x_value = (window_w - self.dimension_grid) // 2
        self.y_value = 0
        self.w_value = self.dimension_grid // self.grid_size
        self.h_value = self.dimension_grid // self.grid_size