"""
Teyeliz - Clase Game
"""

# Import Python modules
import pygame

# Import custom modules
from data.card import Card

# Game class
class Game():
    def __init__(self, p1, p2):
        self.player1 = p1
        self.player2 = p2

        self.played_data1 = None
        self.played_data2 = None

        self.num_round = 1

        # Load the game background and scale it
        self.background = pygame.image.load("resources/graphics/bg/background.png")
        self.background = pygame.transform.scale(self.background, (760, 412))

        # Load the game over screen and scale it
        self.game_over = pygame.image.load("resources/graphics/bg/over.png")
        self.game_over = pygame.transform.scale(self.game_over, (760, 412))

    def select_card(self, player):
        print(f"\nPlayer '{player}':")
        
        while True:
            try:
                card_index = int(input("\nSelect a card to play (1..5): "))
                if card_index >= 1 and card_index <= 5:
                    card_index -= 1
                    break
            except ValueError:
                pass

        if player == self.player1:
            self.played_data1 = player.play_card(card_index)
            self.show_played_card(player, self.played_data1)
            return (card_index, self.played_data1)
        else:
            self.played_data2 = player.play_card(card_index)
            self.show_played_card(player, self.played_data2)
            return (card_index, self.played_data2)
        
    def show_played_card(self, player, data):
        if player == self.player1:
            print(f"\nPlayer '{player}' played card '{self.data_to_card(data)}'\n")
        else:
            print(f"\nPlayer '{player}' played card '{self.data_to_card(data)}'\n")

    def data_to_card(self, data):
        element = data[0]
        color = data[1]
        power = data[2]

        return Card(element, color, power)

    def compare_cards(self, data1, data2):
        self.played_data1 = data1
        self.played_data2 = data2

        print(f"\n=====================================")
        self.show_played_card(self.player1, data1)
        self.show_played_card(self.player2, data2)
        print(f"\n=====================================")

        if self.played_data1[0] == self.played_data2[0]: # Same element
            if self.played_data1[-1] == self.played_data2[-1]: # Same power
                return 0
            elif self.played_data1[-1] > self.played_data2[-1]: # Higher power
                return 1
            else: # Lower power
                return 2
        elif ((self.played_data1[0] == 1 and self.played_data2[0] == 3) or # Fire > Plant
              (self.played_data1[0] == 2 and self.played_data2[0] == 1) or # Water > Fire
              (self.played_data1[0] == 3 and self.played_data2[0] == 2)): # Plant > Water
            return 1
        else: # Other way around
            return 2
        
    def win_round(self, round_winner):
        if round_winner == 0:
            print("\nDraw!\n")
        elif round_winner == 1:
            print(f"\nPlayer '{self.player1}' wins the round!\n")
            self.player1.add_card_to_tictactoe(self.played_data1)
        else:
            print(f"\nPlayer '{self.player2}' wins the round!\n")
            self.player2.add_card_to_tictactoe(self.played_data2)
    
    def show_hud(self, player = None):
        print("\n=====================================")
        print(f"\nRound {self.num_round}")
        print(f"\nPlayer '{self.player1}' tictactoe:\n")
        self.player1.show_tictactoe()
        print(f"\nPlayer '{self.player2}' tictactoe:\n")
        self.player2.show_tictactoe()

        if player == self.player1:
            print(f"\nPlayer '{self.player1}' hand:\n")
            self.player1.show_hand()
        elif player == self.player2:
            print(f"\nPlayer '{self.player2}' hand:\n")
            self.player2.show_hand()
        print("\n=====================================")

    def check_winner(self):
        if self.player1.check_tictactoe():
            return 1
        elif self.player2.check_tictactoe():
            return 2
        else:
            return 0
    
    def win_game(self, game_winner):
        print(f"\n=====================================")
        if game_winner == 1:
            print(f"\nPlayer '{self.player1}' tictactoe:\n")
            self.player1.show_tictactoe()
            print(f"\nPlayer '{self.player1}' wins the game!\n")
        elif game_winner == 2:
            print(f"\nPlayer '{self.player2}' tictactoe:\n")
            self.player2.show_tictactoe()
            print(f"\nPlayer '{self.player2}' wins the game!\n")
        print(f"\n=====================================")

    def new_round(self, card_index1, card_index2):
        self.player1.draw_card(card_index1)
        self.player2.draw_card(card_index2)

        self.num_round += 1