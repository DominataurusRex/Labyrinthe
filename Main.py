import pygame
import sys

pygame.init()

window = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)

# -- Constante --
FONT_HEIGHT = [19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 34, 35, 37,
               38, 40, 41, 43, 44, 46, 47, 49, 50, 52, 53, 55, 56,
               58, 59, 61, 62, 64, 65, 67, 68, 70, 71, 73, 74, 76,
               77, 79, 80, 82, 83, 85, 86, 88, 89, 91, 92, 94, 95,
               97, 98, 100, 101, 103, 104, 106, 107, 109, 110, 112,
               113, 115, 116, 118, 119, 121, 122, 124, 125, 127, 128,
               130, 131, 133, 134, 136, 137, 139, 140, 142, 144, 145,
               147, 148, 150, 151, 153, 154, 156, 157, 159, 160, 162,
               163, 165, 166, 168, 169, 171, 172, 174, 175, 177, 178,
               180, 181, 183, 184, 186, 187, 189, 190, 192, 193, 195,
               196, 198, 199, 201, 202, 204, 205, 207, 208, 210, 211,
               213, 214, 216, 217, 219, 220, 222, 223, 225, 226, 228,
               229, 231, 232, 234, 235, 237, 238, 240, 241, 243, 244,
               246, 247, 249, 250, 252, 253, 255, 256, 258, 259, 261,
               262, 264, 265, 267, 268, 270, 271, 273, 274, 276, 277,
               279, 280, 282, 284, 285, 287, 288, 290, 291, 293, 294,
               296, 297, 299, 300]
COLOR = {'WHITE': (255, 255, 255),
         'BLUE': (0, 59, 111),
         'YELLOW': (255, 215, 0),
         'RED': (207, 10, 29),
         'GREEN': (34, 120, 15)}

# -- Fonction --
def get_font_size(font_height):
    """récupère une valeur de taille de police selon `font_height` un entier
    naturel représentant la hauteur de font voulu en nombre de pixel sur la
    fenêtre de jeu."""
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

# -- Classe --
class Button:
    """
    crée un bouton visuel avec un bouton centré
    """
    def __init__(self, window, relative_position, text, color=COLOR['BLUE']):
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
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, self.color, self.rect, 3)
        surface.blit(self.text_image, self.text_pos)

    def is_pressed(self, event):
        """
        Détecte si le bouton est pressé
        """
        mouse = pygame.mouse.get_pos()
        dimension_x = self.x_value + self.w_value
        dimension_y = self.y_value + self.h_value
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.x_value <= mouse[0] <= dimension_x and self.y_value <= mouse[1] <= dimension_y:
                    return True
        return False


# -- Affichage --
def create_main_menu(window):
    """
    Mise en place de la logique du 'main_menu'
    """
    play_button = Button(window, (0.1, 0.2, 0.1, 0.1), 'Play')
    score_button = Button(window, (0.2, 0.2, 0.1, 0.1), 'Text')
    play_button.draw(window)
    score_button.draw(window)
    pygame.display.flip()
    return play_button, score_button


def main_menu(window):
    """
    Affichage du 'main_menu'
    """
    proceed = True
    play_button, score_button = create_main_menu(window)
    while proceed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                if window_w < 500 or window_h < 250:
                    window = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
                play_button, score_button = create_main_menu(window)
            if play_button.is_pressed(event):
                print("a")
            if score_button.is_pressed(event):
                print('b')
        pygame.display.flip()

main_menu(window)
