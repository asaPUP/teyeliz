"""
Teyeliz - Clase Player
"""

# Importamos los modulos de python
import pygame

# Importamos los modulos del juego
from data.card import Card

# Clase Player
class Player():
    # Constructor
    def __init__(self, s=None, pygame_data=None):
        # Si no se especifica el socket, se asigna 0 (servidor)
        if s is None:
            s = 0

        # Asigna el socket tipo de socket (0 = servidor, 1 = cliente) del jugador
        self.socket = s

        # Inicializa la mano del jugador y su cuadricula
        self.hand = [Card() for i in range(5)]
        self.tictactoe = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]

        # Recibe los datos de pygame
        self.pygame_data = pygame_data

    # Funcion que juega una carta
    def play_card(self, position):
        # Obtiene la carta a jugar
        card = self.hand[position]

        # Guarda los datos de la carta
        element = card.element
        color = card.color
        power = card.power

        data = (element, color, power)

        # Elimina la carta de la mano
        self.hand[position] = None

        # Muestra una carta vacia en la ventana de pygame
        empty_card_image = pygame.image.load("resources/graphics/cards/empty.png")
        empty_card_image = pygame.transform.scale(empty_card_image, (64, 104))
        empty_card_image_rect = empty_card_image.get_rect()
        empty_card_image_rect.topleft = (138 + (106 * position), 259)
        self.pygame_data[1].blit(empty_card_image, empty_card_image_rect)

        # Muestra la carta jugada en la ventana de pygame
        card_image = card.image
        card_image = pygame.transform.scale(card_image, (96, 156))
        card_image_rect = card_image.get_rect()
        if self.socket == 0:
            card_image_rect.topleft = (254, 60)
        else:
            card_image_rect.topleft = (410, 60)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

        return data

    # Funcion que obtiene una nueva carta
    def draw_card(self, position):
        self.hand[position] = Card()

    # Funcion que agrega una carta a la cuadricula
    def add_card_to_tictactoe(self, data):
        element = data[0]
        color = data[1]

        self.tictactoe[element - 1][color - 1] = 1

    # Funcion que revisa si el jugador gano el juego
    def check_tictactoe(self):
        # Revisa si el jugador lleno una fila de su cuadricula
        for i in range(3):
            if self.tictactoe[i][0] == self.tictactoe[i][1] == self.tictactoe[i][2] == 1:
                return True

        # Revisa si el jugador lleno una columna de su cuadricula
        for j in range(3):
            if self.tictactoe[0][j] == self.tictactoe[1][j] == self.tictactoe[2][j] == 1:
                return True

        return False

    # Funcion que muestra la mano del jugador
    def show_hand(self):
        # Muestra las cartas en la ventana de pygame
        for i in range(5):
            card = self.hand[i]
            card_image = card.image
            card_image = pygame.transform.scale(card_image, (64, 104))
            card_image_rect = card_image.get_rect()
            card_image_rect.topleft = (138 + (106 * i), 259)
            self.pygame_data[1].blit(card_image, card_image_rect)
        
        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

    # Funcion que muestra la cuadricula del jugador
    def show_tictactoe(self):
        # Lista de elementos y colores
        element = ["Tletl", "Atl", "Metl"]
        color = ["Rosa", "Turquesa", "Dorado"]

        for i in range(3):
            for j in range(3):
                # Si la casilla no esta vacia, muestra la miniatura de la carta
                if self.tictactoe[i][j] == 1:
                    thumbnail = pygame.image.load(f"resources/graphics/thumbnails/{element[i]}/{element[i]}{color[j]}.png")
                    thumbnail = pygame.transform.scale(thumbnail, (32, 32))
                    thumbnail_rect = thumbnail.get_rect()
                    if self.socket == 0:
                        thumbnail_rect.topleft = (73 + (50 * j), 72 + (50 * i))
                    else:
                        thumbnail_rect.topleft = (556 + (50 * j), 72 + (50 * i))
                    self.pygame_data[1].blit(thumbnail, thumbnail_rect)

        # Actualiza la ventana de pygame
        self.pygame_data[0].flip()

    # Define el metodo de string de la clase
    def __str__(self):
        if self.socket == 0:
            return "Servidor"
        else:
            return "Cliente"

    # Define el metodo de representacion de la clase
    def __repr__(self):
        return self.__str__()
