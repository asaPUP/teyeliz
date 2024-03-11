"""
Teyeliz - Game Class
"""

# Import Python modules
import pygame
import time

# Import game modules
from data.card import Card

# Game class
class Game():
    # Constructor
    def __init__(self, p1, p2, pygame_data):
        # Create players
        self.player1 = p1
        self.player2 = p2

        # Create variables for played cards
        self.played_data1 = None
        self.played_data2 = None

        # Create variable for the round number
        self.num_round = 1

        # Load and scale game background
        self.background = pygame.image.load("resources/graphics/bg/background.png")
        self.background = pygame.transform.scale(self.background, (760, 412))

        # Load and scale game over screen
        self.game_over = pygame.image.load("resources/graphics/bg/over.png")
        self.game_over = pygame.transform.scale(self.game_over, (760, 412))

        # Load game logo
        self.logo = pygame.image.load("resources/graphics/logo/logo.png")

        # Receive pygame data
        self.pygame_data = pygame_data

    # Function to select a card
    def select_card(self, player):
        # Clear event queue
        pygame.event.clear()

        # Wait for player to press a key from 1 to 5 to select a card
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
            
            # If player selected a card, exit loop
            if card_index is not None:
                break
        
        # Play the selected card
        if player == self.player1:
            self.played_data1 = player.play_card(card_index)
            self.show_played_card(player, self.played_data1)
            return (card_index, self.played_data1)
        else:
            self.played_data2 = player.play_card(card_index)
            self.show_played_card(player, self.played_data2)
            return (card_index, self.played_data2)
    
    # Function to display the played card
    def show_played_card(self, player, data):
        # Convert card data to a Card object
        card = self.data_to_card(data)

        # Load the image corresponding to the played card
        card_image = card.image
        card_image = pygame.transform.scale(card_image, (96, 156))
        card_image_rect = card_image.get_rect()

        # Show the card on the pygame window
        if player == self.player1:
            card_image_rect.topleft = (254, 60)
        else:
            card_image_rect.topleft = (410, 60)
        self.pygame_data[1].blit(card_image, card_image_rect)

        # Update the pygame window
        self.pygame_data[0].flip()

    # Function to convert card data to a Card object
    def data_to_card(self, data):
        element = data[0]
        color = data[1]
        power = data[2]

        return Card(element, color, power)

    # Function to compare played cards
    def compare_cards(self, data1, data2):
        # Save played card data
        self.played_data1 = data1
        self.played_data2 = data2

        # Display played cards on the pygame window
        self.show_played_card(self.player1, data1)
        self.show_played_card(self.player2, data2)

        # Wait for 1 second
        time.sleep(1)

        # Load comparison text and scale it
        font = self.pygame_data[2]
        draw_text = font.render("=", True, (255, 255, 255))
        draw_text = pygame.transform.scale(draw_text, (draw_text.get_width() * 5, draw_text.get_height() * 5))
        left_text = font.render(">", True, (255, 255, 255))
        left_text = pygame.transform.scale(left_text, (left_text.get_width() * 5, left_text.get_height() * 5))
        right_text = font.render("<", True, (255, 255, 255))
        right_text = pygame.transform.scale(right_text, (right_text.get_width() * 5, right_text.get_height() * 5))
        position = (384, 150)

        # Compare played cards and return the round winner
        if self.played_data1[0] == self.played_data2[0]:  # Same element
            if self.played_data1[-1] == self.played_data2[-1]:  # Same power
                # Display "=" in the middle of the pygame window
                text = draw_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 0
            
            elif self.played_data1[-1] > self.played_data2[-1]:  # Higher power
                # Display ">" in the middle of the pygame window
                text = left_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 1
            
            else:  # Lower power
                # Display "<" in the middle of the pygame window
                text = right_text
                text_rect = text.get_rect()
                text_rect.center = position
                self.pygame_data[1].blit(text, text_rect)
                self.pygame_data[0].flip()

                time.sleep(2)

                return 2
        
        # Different element
        elif ((self.played_data1[0] == 1 and self.played_data2[0] == 3) or  # Tletl > Metl
              (self.played_data1[0] == 2 and self.played_data2[0] == 1) or  # Atl > Tletl
              (self.played_data1[0] == 3 and self.played_data2[0] == 2)):  # Metl > Atl
            
            # Display ">" in the middle of the pygame window
            text = left_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 1
        
        else:  # Other cases
            # Display "<" in the middle of the pygame window
            text = right_text
            text_rect = text.get_rect()
            text_rect.center = position
            self.pygame_data[1].blit(text, text_rect)
            self.pygame_data[0].flip()

            time.sleep(2)

            return 2
    
    # Function to display the round result
    def win_round(self, round_winner):
        if round_winner == 0:
            pass  # Do nothing
        elif round_winner == 1:  # Player 1 wins
            self.player1.add_card_to_tictactoe(self.played_data1)
        else:  # Player 2 wins
            self.player2.add_card_to_tictactoe(self.played_data2)
        
        # Display HUD for both players
        self.player1.show_tictactoe()
        self.player2.show_tictactoe()
    
    # Function to display the game HUD
    def show_hud(self, player=None):
        # Display game background
        self.pygame_data[1].blit(self.background, (0, 0))

        # Display round number
        font = self.pygame_data[2]
        text = font.render(f"{self.num_round}", True, (255, 255, 255))
        text_ronda = font.render("ROUND", True, (255, 255, 255))

        # Scale text and display it on the pygame window
        text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
        text_rect = text.get_rect()
        text_rect.center = (380, 26)
        self.pygame_data[1].blit(text, text_rect)

        text_ronda = pygame.transform.scale(text_ronda, (int(text_ronda.get_width() * 0.8), int(text_ronda.get_height() * 0.8)))
        text_rect_ronda = text_ronda.get_rect()
        text_rect_ronda.center = (380, 10)
        self.pygame_data[1].blit(text_ronda, text_rect_ronda)

        # Display "YOU" and "OPPONENT" on the pygame window as needed
        text_you = font.render("YOU", True, (255, 255, 255))
        text_you = pygame.transform.scale(text_you, (text_you.get_width() * 2, text_you.get_height() * 2))
        text_rect_you = text_you.get_rect()

        text_opponent = font.render("OPPONENT", True, (255, 255, 255))
        text_opponent = pygame.transform.scale(text_opponent, (text_opponent.get_width() * 2, text_opponent.get_height() * 2))
        text_rect_opponent = text_opponent.get_rect()

        if player == self.player1:
            text_rect_you.center = (140, 48)
            self.pygame_data[1].blit(text_you, text_rect_you)
            text_rect_opponent.center = (620, 48)
            self.pygame_data[1].blit(text_opponent, text_rect_opponent)
        elif player == self.player2:
            text_rect_you.center = (620, 48)
            self.pygame_data[1].blit(text_you, text_rect_you)
            text_rect_opponent.center = (140, 48)
            self.pygame_data[1].blit(text_opponent, text_rect_opponent)

        # Display game logo
        logo_rect = self.logo.get_rect()
        logo_rect.center = (380, 395)
        self.pygame_data[1].blit(self.logo, logo_rect)

        # Display tic-tac-toe grid for each player
        self.player1.show_tictactoe()
        self.player2.show_tictactoe()

        # Display each player's hand
        if player == self.player1:
            self.player1.show_hand()
        elif player == self.player2:
            self.player2.show_hand()

        # Update the pygame window
        self.pygame_data[0].flip()

    # Function to determine the game winner
    def check_winner(self):
        if self.player1.check_tictactoe():
            return 1
        elif self.player2.check_tictactoe():
            return 2
        else:
            return 0  # No winner

    # Function to display the end game screen
    def win_game(self, game_winner, player):
        # Display the end game screen
        self.pygame_data[1].blit(self.game_over, (0, 0))

        # Display a message depending on who won the game
        if game_winner == player:
            text = self.pygame_data[2].render("YOU WON!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        else:
            text = self.pygame_data[2].render("YOU LOST!", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 3, text.get_height() * 3))
        
        text2 = self.pygame_data[2].render("[ANY KEY] to close...", True, (255, 255, 255))
        text2 = pygame.transform.scale(text2, (text2.get_width() * 2, text2.get_height() * 2))
        
        text_rect = text.get_rect()
        text_rect.center = (380, 250)
        text_rect2 = text2.get_rect()
        text_rect2.center = (380, 300)
        self.pygame_data[1].blit(text, text_rect)
        self.pygame_data[1].blit(text2, text_rect2)

        # Update the pygame window
        self.pygame_data[0].flip()

    # Function to start a new round
    def new_round(self, card_index1, card_index2):
        # Add a card to each player's hand
        self.player1.draw_card(card_index1)
        self.player2.draw_card(card_index2)

        self.num_round += 1  # Increase the round number by 1
    
    # Function to quit the game
    def quit_game(self):
        pygame.quit()
        quit()
