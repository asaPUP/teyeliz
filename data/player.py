"""
Teyeliz - Clase Player
"""

# Import Python modules
import pygame

# Import custom modules
from data.card import Card

# Player class


class Player():
    def __init__(self, s=None, pygame_data=None):
        if s is None:
            s = 0  # Player is the server

        self.socket = s
        self.hand = [Card() for i in range(5)]
        self.tictactoe = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]

        # Pyagme data = [pygame.display, window, font]
        self.pygame_data = pygame_data

    def play_card(self, position):
        element = self.hand[position].element
        color = self.hand[position].color
        power = self.hand[position].power

        elements = ["Tletl", "Atl", "Metl"]
        colors = ["Rosa", "Turquesa", "Dorado"]

        data = (element, color, power)

        self.hand[position] = None

        # Show empty card image in the pygame window in the position of the played card
        # Each card is 32 x 52 pixels, scalet to 64 x 104 pixels

        card_image = pygame.image.load("resources/graphics/cards/empty.png")
        card_image = pygame.transform.scale(card_image, (64, 104))
        card_image_rect = card_image.get_rect()
        card_image_rect.topleft = (138 + (106 * position), 259)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Show the played card in the pygame window
        # Scale the card to 96 x 156 pixels
        # Put the card in the topleft = (254, 60) if the player is the server, (410, 60) if the player is the client
        card_image = pygame.image.load(f"resources/graphics/cards/{elements[element - 1]}/{elements[element - 1]}{colors[color - 1]}{power}.png")
        card_image = pygame.transform.scale(card_image, (96, 156))
        card_image_rect = card_image.get_rect()
        if self.socket == 0:
            card_image_rect.topleft = (254, 60)
        else:
            card_image_rect.topleft = (410, 60)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Update the pygame window
        self.pygame_data[0].flip()

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
        # Show the player's hand in the pygame window
        # Each card is 32 x 52 pixels, scalet to 64 x 104 pixels
        for i in range(5):
            card = self.hand[i]
            card_image = card.image
            card_image = pygame.transform.scale(card_image, (64, 104))
            card_image_rect = card_image.get_rect()
            card_image_rect.topleft = (138 + (106 * i), 259)
            self.pygame_data[1].blit(card_image, card_image_rect)
        # Update the pygame window
        self.pygame_data[0].flip()

    def show_tictactoe(self):
        # Show the player's tictactoe in the pygame window
        # Each thumbnail is 32 x 32 pixels
        element = ["Tletl", "Atl", "Metl"]
        color = ["Rosa", "Turquesa", "Dorado"]

        for i in range(3):
            for j in range(3):
                if self.tictactoe[i][j] == 1:
                    thumbnail = pygame.image.load(f"resources/graphics/thumbnails/{element[i]}/{element[i]}{color[j]}.png")
                    thumbnail = pygame.transform.scale(thumbnail, (32, 32))
                    thumbnail_rect = thumbnail.get_rect()
                    if self.socket == 0:
                        thumbnail_rect.topleft = (73 + (50 * j), 72 + (50 * i))
                    else:
                        thumbnail_rect.topleft = (556 + (50 * j), 72 + (50 * i))
                    self.pygame_data[1].blit(thumbnail, thumbnail_rect)
        # Update the pygame window
        self.pygame_data[0].flip()

    def __str__(self):
        if self.socket == 0:
            return "Servidor"
        else:
            return "Cliente"

    def __repr__(self):
        return self.__str__()
