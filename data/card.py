"""
Teyeliz - Clase Card
"""

# Importamos los modulos de python
from random import randint
import pygame

# Clase Card
class Card():
    # Constructor
    def __init__(self, e=None, c=None, p=None):
        # Si no se especifica el elemento, color o poder de la carta, se asigna uno aleatorio
        if e is None:
            e = randint(1, 3)
        if c is None:
            c = randint(1, 3)
        if p is None:
            p = randint(1, 4)

        # Lista de elementos y colores
        self.elements = ["Tletl", "Atl", "Metl"] # Fuego, Agua, Planta
        self.colors = ["Rosa", "Turquesa", "Dorado"]
        
        # Asigna los valores de la carta
        self.element = e
        self.color = c
        self.power = p

        # Tamaño de la carta y su miniatura
        self.IMAGE_SIZE = (32, 52)
        self.THUMBNAIL_SIZE = (32, 32)

        # Carga la imagen de la carta y la escala
        self.image = pygame.image.load(f"resources/graphics/cards/{self.elements[self.element - 1]}/{self.elements[self.element - 1]}{self.colors[self.color - 1]}{self.power}.png")
        self.image = pygame.transform.scale(self.image, self.IMAGE_SIZE)

        # Cargo la miniatura de la carta y la escala
        self.thumbnail = pygame.image.load(f"resources/graphics/thumbnails/{self.elements[self.element - 1]}/{self.elements[self.element - 1]}{self.colors[self.color - 1]}.png")
        self.thumbnail = pygame.transform.scale(self.thumbnail, self.THUMBNAIL_SIZE)

    # Define el metodo de string de la clase
    def __str__(self):
        return f"{self.elements[self.element - 1]} | {self.colors[self.color - 1]} | {self.power}"
    
    # Define el metodo de representacion de la clase
    def __repr__(self):
        return self.__str__()