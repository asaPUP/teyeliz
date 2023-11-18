"""
Teyeliz - Clase Game
"""

# Import Python modules
import pygame
import time

# Import custom modules
from data.card import Card

# Game class
class Game():
    def __init__(self, p1, p2, pygame_data):
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

        # Pyagme data = [pygame.display, window, font]
        self.pygame_data = pygame_data

    def select_card(self, player):
        # Select a card to play from the pygame window instead of the console
        pygame.event.clear()

        card_index = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        card_index = 0
                        break
                    elif event.key == pygame.K_2:
                        card_index = 1
                        break
                    elif event.key == pygame.K_3:
                        card_index = 2
                        break
                    elif event.key == pygame.K_4:
                        card_index = 3
                        break
                    elif event.key == pygame.K_5:
                        card_index = 4
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                elif event.type == pygame.QUIT:
                    self.quit_game()
            
            if card_index is not None:
                break

        if player == self.player1:
            self.played_data1 = player.play_card(card_index)
            self.show_played_card(player, self.played_data1)
            return (card_index, self.played_data1)
        else:
            self.played_data2 = player.play_card(card_index)
            self.show_played_card(player, self.played_data2)
            return (card_index, self.played_data2)
        
    def show_played_card(self, player, data):
        # Show the played card in the pygame window
        # Scale the card to 96 x 156 pixels
        # Put the card in the topleft = (254, 60) if the player is the server, (410, 60) if the player is the client
        element = data[0]
        color = data[1]
        power = data[2]

        elements = ["Tletl", "Atl", "Metl"]
        colors = ["Rosa", "Turquesa", "Dorado"]

        card_image = pygame.image.load(f"resources/graphics/cards/{elements[element - 1]}/{elements[element - 1]}{colors[color - 1]}{power}.png")
        card_image = pygame.transform.scale(card_image, (96, 156))
        card_image_rect = card_image.get_rect()
        if player == self.player1:
            card_image_rect.topleft = (254, 60)
        else:
            card_image_rect.topleft = (410, 60)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Update the pygame window
        self.pygame_data[0].flip()

    def data_to_card(self, data):
        element = data[0]
        color = data[1]
        power = data[2]

        return Card(element, color, power)

    def compare_cards(self, data1, data2):
        self.played_data1 = data1
        self.played_data2 = data2

        self.show_played_card(self.player1, data1)
        self.show_played_card(self.player2, data2)

        time.sleep(1)

        font = self.pygame_data[2]
        draw_text = font.render("=", True, (255, 255, 255))
        draw_text = pygame.transform.scale(draw_text, (draw_text.get_width() * 5, draw_text.get_height() * 5))
        left_text = font.render(">", True, (255, 255, 255))
        left_text = pygame.transform.scale(left_text, (left_text.get_width() * 5, left_text.get_height() * 5))
        right_text = font.render("<", True, (255, 255, 255))
        right_text = pygame.transform.scale(right_text, (right_text.get_width() * 5, right_text.get_height() * 5))
        position = (384, 150)

        if self.played_data1[0] == self.played_data2[0]: # Same element
            if self.played_data1[-1] == self.played_data2[-1]: # Same power
                # Show a big "=" in the middle of the pygame window
                text = draw_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 0
            
            elif self.played_data1[-1] > self.played_data2[-1]: # Higher power
                # Show a big ">" in the middle of the pygame window
                text = left_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 1
            
            else: # Lower power
                # Show a big "<" in the middle of the pygame window
                text = right_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 2
            
        elif ((self.played_data1[0] == 1 and self.played_data2[0] == 3) or # Fire > Plant
              (self.played_data1[0] == 2 and self.played_data2[0] == 1) or # Water > Fire
              (self.played_data1[0] == 3 and self.played_data2[0] == 2)): # Plant > Water
            # Show a big ">" in the middle of the pygame window
            text = left_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 1
        
        else: # Other way around
            # Show a big "<" in the middle of the pygame window
            text = right_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 2
        
    def win_round(self, round_winner):
        if round_winner == 0:
            pass # Do nothing
        elif round_winner == 1:
            self.player1.add_card_to_tictactoe(self.played_data1)
        else:
            self.player2.add_card_to_tictactoe(self.played_data2)
    
    def show_hud(self, player = None):
        # Show the game background
        self.pygame_data[1].blit(self.background, (0, 0))

        # Show the round number
        font = self.pygame_data[2]
        text = font.render(f"{self.num_round}", True, (255, 255, 255))
        # Resize the text
        text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
        text_rect = text.get_rect()
        text_rect.center = (380, 20)
        self.pygame_data[1].blit(text, text_rect)

        self.player1.show_tictactoe()
        self.player2.show_tictactoe()

        if player == self.player1:
            self.player1.show_hand()
        elif player == self.player2:
            self.player2.show_hand()

        # Update the pygame window
        self.pygame_data[0].flip()

    def check_winner(self):
        if self.player1.check_tictactoe():
            return 1
        elif self.player2.check_tictactoe():
            return 2
        else:
            return 0
    
    def win_game(self, game_winner, player):
        # Show the game over screen
        self.pygame_data[1].blit(self.game_over, (0, 0))

        # Show if the player won or lost
        if game_winner == player:
            text = self.pygame_data[2].render("You win!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        else:
            text = self.pygame_data[2].render("You lose!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        
        text2 = self.pygame_data[2].render("Press ANY KEY to exit...", True, (255, 255, 255))
        text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))
        
        text_rect = text.get_rect()
        text_rect.center = (380, 250)
        text_rect2 = text2.get_rect()
        text_rect2.center = (380, 300)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)

        self.pygame_data[0].flip()

    def new_round(self, card_index1, card_index2):
        self.player1.draw_card(card_index1)
        self.player2.draw_card(card_index2)

        self.num_round += 1
    
    def quit_game(self):
        pygame.quit()
        quit()