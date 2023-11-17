"""
Teyetest - Clase Card
"""

# Import Python modules
from random import randint
import pygame

# Import custom modules

# Card class
class Card():
    def __init__(self, e=None, c=None, p=None):
        if e is None:
            e = randint(1, 3)
        if c is None:
            c = randint(1, 3)
        if p is None:
            p = randint(1, 4)

        self.elements = ["Tletl", "Atl", "Metl"] # Fuego, Agua, Planta
        self.colors = ["Rosa", "Turquesa", "Dorado"]
        
        self.element = e
        self.color = c
        self.power = p

        self.IMAGE_SIZE = (32, 52)
        self.THUMBNAIL_SIZE = (32, 32)

        # Image depends of the cards element, color and power
        self.image = pygame.image.load(f"resources/graphics/cards/{self.elements[self.element - 1]}/
                                       {self.elements[self.element - 1]}{self.colors[self.color - 1]}{self.power}.png")
        self.image = pygame.transform.scale(self.image, self.IMAGE_SIZE)

        # Thumbnail depends of the cards element and color, not power
        self.thumbnail = pygame.image.load(f"resources/graphics/thumbnails/{self.elements[self.element - 1]}/
                                           {self.elements[self.element - 1]}{self.colors[self.color - 1]}.png")
        self.thumbnail = pygame.transform.scale(self.thumbnail, self.THUMBNAIL_SIZE)

    def __str__(self):
        return f"{self.elements[self.element - 1]} | {self.colors[self.color - 1]} | {self.power}"
    
    def __repr__(self):
        return self.__str__()