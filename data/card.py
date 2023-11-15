"""
Teyetest - Clase Card
"""

# Import Python modules
from random import randint

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
        
        self.element = e
        self.color = c
        self.power = p

    def __str__(self):
        elements = ["Fuego", "Agua", "Planta"]
        colors = ["Rosa", "Turquesa", "Amarillo"]

        return f"{elements[self.element - 1]} | {colors[self.color - 1]} | {self.power}"
    
    def __repr__(self):
        return self.__str__()