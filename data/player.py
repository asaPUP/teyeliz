"""
Teyetest - Clase Player
"""

# Import Python modules

# Import custom modules
from data.card import Card

# Player class
class Player():
    def __init__(self, s=None):
        if s is None:
            s = 0 # Player is the server
        
        self.socket = s
        self.hand = [Card() for i in range(5)]
        self.tictactoe = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        
    def play_card(self, position):
        element = self.hand[position].element
        color = self.hand[position].color
        power = self.hand[position].power

        data = (element, color, power)

        self.hand[position] = None

        return data
    
    def draw_card(self, position):
        self.hand[position] = Card()
    
    def add_card_to_tictactoe(self, data):
        element = data[0]
        color = data[1]

        self.tictactoe[element - 1][color - 1] = 1

    def check_tictactoe(self):
        for i in range(3):
            if self.tictactoe[i][0] == self.tictactoe[i][1] == self.tictactoe[i][2] == 1:
                return True

        for j in range(3):
            if self.tictactoe[0][j] == self.tictactoe[1][j] == self.tictactoe[2][j] == 1:
                return True
        
        return False

    def show_hand(self):
        for i in range(5):
            print(f"{i + 1}. {self.hand[i]}")
    
    def show_tictactoe(self):
        print("  R T A") # R = Rosa, T = Turquesa, A = Amarillo
        for i in range(3):
            if i == 0:      # Fuego
                print("F", end=" ")
            elif i == 1:    # Agua
                print("A", end=" ")
            else:           # Planta
                print("P", end=" ")
            for j in range(3):
                print(f"{self.tictactoe[i][j]}", end=" ")
            print()
    
    def __str__(self):
        if self.socket == 0:
            return "Server"
        else:
            return "Client"
        
    def __repr__(self):
        return self.__str__()