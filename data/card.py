"""
Teyeliz - Card Class
"""

# Import Python modules
from random import randint
import pygame

# Card class
class Card():
    # Constructor
    def __init__(self, e=None, c=None, p=None):
        # If element, color, or power of the card is not specified, assign a random one
        if e is None:
            e = randint(1, 3)
        if c is None:
            c = randint(1, 3)
        if p is None:
            p = randint(1, 4)

        # List of elements and colors
        self.elements = ["Tletl", "Atl", "Metl"]  # Fire, Water, Plant
        self.colors = ["Pink", "Turquoise", "Gold"]
        
        # Assign card values
        self.element = e
        self.color = c
        self.power = p

        # Card size and thumbnail size
        self.IMAGE_SIZE = (32, 52)
        self.THUMBNAIL_SIZE = (32, 32)

        # Load card image and scale it
        self.image = pygame.image.load(f"resources/graphics/cards/{self.elements[self.element - 1]}/{self.elements[self.element - 1]}{self.colors[self.color - 1]}{self.power}.png")
        self.image = pygame.transform.scale(self.image, self.IMAGE_SIZE)

        # Load card thumbnail and scale it
        self.thumbnail = pygame.image.load(f"resources/graphics/thumbnails/{self.elements[self.element - 1]}/{self.elements[self.element - 1]}{self.colors[self.color - 1]}.png")
        self.thumbnail = pygame.transform.scale(self.thumbnail, self.THUMBNAIL_SIZE)

    # Define the string method of the class
    def __str__(self):
        return f"{self.elements[self.element - 1]} | {self.colors[self.color - 1]} | {self.power}"
    
    # Define the representation method of the class
    def __repr__(self):
        return self.__str__()
